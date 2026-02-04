from django.db import models
from django.utils import timezone
from django.db.models import Sum

class Parents(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    birth_date = models.DateField(null=True, blank=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='descendants'
    )

    def __str__(self):
        return self.name



class Children(models.Model):
    
    parent = models.ForeignKey(Parents, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

    class Meta:
        verbose_name_plural = "Children"

    def __str__(self):
        return f"{self.name} (Child of {self.parent.name})"
    


class Event(models.Model):
    EVENT_TYPES = [
        ('Wedding', 'Wedding'),
        ('Party', 'Party'),
        ('Funeral', 'Funeral'),
        ('Other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=EVENT_TYPES)
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



class Contribution(models.Model):
    event = models.ForeignKey(Event, related_name='contributions', on_delete=models.CASCADE)
    member_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)



class Asset(models.Model):
    CATEGORY_CHOICES = [
        ('LAND', 'Land'),
        ('BUILDING', 'Building'),
        ('VEHICLE', 'Vehicle'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    valuation = models.DecimalField(max_digits=15, decimal_places=2)
    location = models.CharField(max_length=200, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_contributed(self):
        return sum(owner.share for owner in self.owners.all())

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

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
