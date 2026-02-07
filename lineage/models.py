from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class Parents(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='descendants'
    )
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=Parents)
def create_user_for_parent(sender, instance, created, **kwargs):
    if created:
        birth_year = instance.birth_date.year if instance.birth_date else "0000"
        base_username = instance.name.strip()
        username = base_username
        count = 1
        while User.objects.filter(username__iexact=username).exists():
            username = f"{base_username} ({count})"
            count += 1
        User.objects.create_user(
            username=username,
            password=str(birth_year)
        )


class Children(models.Model):
    parent = models.ForeignKey(Parents, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Children"

    def __str__(self):
        return f"{self.name} (Child of {self.parent.name})"
    
@receiver(post_save, sender=Children)
def create_user_for_child(sender, instance, created, **kwargs):
    if created:
        birth_year = instance.birth_date.year if instance.birth_date else "0000"
        base_username = instance.name.strip()
        username = base_username
        count = 1
        while User.objects.filter(username__iexact=username).exists():
            username = f"{base_username} ({count})"
            count += 1
        User.objects.create_user(
            username=username,
            password=str(birth_year)
        )


class EventType(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    def __str__(self):
        return self.name
    
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
        result = self.contributions.aggregate(total=Sum('amount'))['total']
        return result or 0
    @property
    def is_past(self):
        from django.utils import timezone
        return self.date < timezone.now().date()


class Family(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Contribution(models.Model):
    event = models.ForeignKey(Event, related_name='contributions', on_delete=models.CASCADE)
    family = models.ForeignKey(Family, related_name='contributions', on_delete=models.SET_NULL, null=True, blank=True)
    member_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member_name} - {self.event.title}"



class AssetCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Asset(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    valuation = models.DecimalField(max_digits=15, decimal_places=2)
    location = models.CharField(max_length=200, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_contributed(self):
        return sum(owner.share for owner in self.owners.all())

    def __str__(self):
        return f"{self.title} ({self.category.name if self.category else 'No Category'})"


class Owner(models.Model):
    asset = models.ForeignKey(
        Asset, 
        related_name='owners', 
        on_delete=models.CASCADE
    )
    member_name = models.CharField(max_length=150)
    share = models.DecimalField(
        max_digits=12, decimal_places=2,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member_name} - {self.asset.title} (Ksh {self.share})"
