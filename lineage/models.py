from datetime import date

from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# -------------------------
# PERSON
# -------------------------
class Person(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    STATUS_CHOICES = [('alive', 'Alive'), ('deceased', 'Deceased')]
    JOB_CHOICES = [('employed', 'Employed'), ('unemployed', 'Unemployed')]
    DISABILITY_CHOICES = [
        ('none', 'None'),
        ('physical', 'Physical'),
        ('mental', 'Mental'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='alive'
    )
    job_status = models.CharField(
        max_length=20, choices=JOB_CHOICES, default='unemployed'
    )
    disability_status = models.CharField(
        max_length=20, choices=DISABILITY_CHOICES, default='none'
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    father = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='children_from_father',
        on_delete=models.SET_NULL
    )

    mother = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='children_from_mother',
        on_delete=models.SET_NULL
    )

    spouse = models.OneToOneField(
        'self',
        null=True,
        blank=True,
        related_name='married_to',
        on_delete=models.SET_NULL
    )

    photo = models.ImageField(upload_to='members/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # -------------------------
    # ANCESTORS
    # -------------------------
    def get_father_ancestors(self, max_depth=5):
        ancestors, current, depth = [], self.father, 0

        while current and depth < max_depth:
            ancestors.append(current)
            current = current.father
            depth += 1

        return ancestors

    # -------------------------
    # DESCENDANTS (DRY)
    # -------------------------
    def get_children(self):
        return Person.objects.filter(
            Q(father=self) | Q(mother=self)
        ).distinct()

    def _get_descendants(self, depth):
        current_generation = self.get_children()

        for _ in range(depth - 1):
            next_generation = Person.objects.none()
            for person in current_generation:
                next_generation |= person.get_children()
            current_generation = next_generation.distinct()

        return current_generation

    def get_grandchildren(self):
        return self._get_descendants(2)

    def get_great_grandchildren(self):
        return self._get_descendants(3)

    # -------------------------
    # AGE
    # -------------------------
    def get_age(self):
        if not self.birth_date:
            return None

        today = date.today()
        age = today.year - self.birth_date.year

        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1

        return age

    # -------------------------
    # SIBLINGS
    # -------------------------
    def get_siblings(self):
        query = Q()

        if self.father:
            query |= Q(father=self.father)

        if self.mother:
            query |= Q(mother=self.mother)

        if not query:
            return Person.objects.none()

        return Person.objects.filter(query).exclude(id=self.id).distinct()


# -------------------------
# EVENT TYPES
# -------------------------
class EventType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# -------------------------
# EVENTS
# -------------------------
class Event(models.Model):
    title = models.CharField(max_length=200)
    type = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True)

    family_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date = models.DateField()

    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.family_name})"

    @property
    def total_contributed(self):
        return (
            self.contributions.aggregate(total=Sum('amount'))['total']
            or 0
        )

    @property
    def is_past(self):
        return self.date < timezone.now().date()

    @property
    def remaining_amount(self):
        remaining = self.goal_amount - self.total_contributed
        return remaining if remaining > 0 else 0


# -------------------------
# CONTRIBUTIONS
# -------------------------
class Contribution(models.Model):
    event = models.ForeignKey(
        Event,
        related_name="contributions",
        on_delete=models.CASCADE
    )
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    contributed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} -> {self.event} ({self.amount})"


# -------------------------
# ASSETS
# -------------------------
class Asset(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        'AssetCategory',  # Assuming you have an AssetCategory model defined elsewhere
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assets'
    )

    valuation = models.DecimalField(max_digits=15, decimal_places=2)
    location = models.CharField(max_length=200, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_contributed(self):
        return self.owners.aggregate(
            total=Sum('share')
        )['total'] or 0

    def __str__(self):
        category = self.category.name if self.category else "No Category"
        return f"{self.title} ({category})"
