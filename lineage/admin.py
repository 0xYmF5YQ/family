from django.contrib import admin
#from .models import (Parents, Children, EventType, Event, Family, Contribution, AssetCategory, Asset, Owner)
from .models import (EventType, Event, Contribution, AssetCategory, Asset, Owner, Family)

"""class ChildrenInline(admin.TabularInline):
    model = Children
    extra = 1
    fields = ('name', 'gender', 'birth_date')


@admin.register(Parents)
class ParentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'birth_date', 'user', 'parent')
    list_filter = ('gender', 'birth_date')
    search_fields = ('name',) 
    
    
    autocomplete_fields = ['parent'] 
    inlines = [ChildrenInline]

@admin.register(Children)
class ChildrenAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'birth_date', 'user')
    readonly_fields = ('get_siblings',)
    fields = ('parent', 'name', 'gender', 'birth_date', 'user', 'get_siblings')
    
    autocomplete_fields = ['parent'] 

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        if 'parent' in request.GET:
            initial['parent'] = request.GET.get('parent')
        return initial

    def get_siblings(self, obj):
        if not obj.id or not obj.parent:
            return "No siblings found."
        siblings = Children.objects.filter(parent=obj.parent).exclude(id=obj.id)
        return ", ".join([s.name for s in siblings]) if siblings.exists() else "No siblings found."

    get_siblings.short_description = "Siblings"
"""

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'family_name', 'date', 'goal_amount', 'is_active')
    list_filter = ('is_active', 'date', 'type')
    search_fields = ('title', 'family_name')

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'event', 'amount', 'family', 'created_at')
    list_filter = ('event', 'family')
    search_fields = ('member_name',)

class OwnerInline(admin.TabularInline):
    model = Owner
    extra = 1

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'valuation', 'location', 'size')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'location')
    inlines = [OwnerInline] 



admin.site.register(EventType)
admin.site.register(Family)
admin.site.register(AssetCategory)
admin.site.register(Owner)