from django.contrib import admin
from .models import EventType, Event, Contribution, Asset, Person, AssetOwnership

admin.site.register(Person)
admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(Contribution)
admin.site.register(Asset)
admin.site.register(AssetOwnership)
