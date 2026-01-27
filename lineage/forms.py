from django import forms
from .models import Person
from .models import Contribution, Event
from .models import Asset, Owner

class ParentForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'birth_date', 'parent'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500', 'placeholder': 'Full Name'}),
            'birth_date': forms.DateInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500', 'type': 'date'}),
            'parent': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Person.objects.filter(is_parent=True)
        self.fields['parent'].required = False 
        self.fields['parent'].label = "Parent (optional)"

class ChildForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'birth_date', 'parent']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full pl-4 pr-4 py-3 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Enter full name'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'parent': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Person.objects.filter(is_parent=True)
        self.fields['parent'].empty_label = "Select parent"

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'type',
            'family_name',
            'location',
            'date',
            'goal_amount',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border-slate-300'
            }),
            'type': forms.Select(attrs={
                'class': 'w-full rounded-xl border-slate-300'
            }),
            'family_name': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border-slate-300'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border-slate-300'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full rounded-xl border-slate-300'
            }),
            'goal_amount': forms.NumberInput(attrs={
                'class': 'w-full rounded-xl border-slate-300',
                'min': 0
            }),
        }


class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['event', 'member_name', 'amount']
        widgets = {
            'event': forms.Select(attrs={
                'class': 'w-full rounded-xl border-slate-300'
            }),
            'member_name': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border-slate-300'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full rounded-xl border-slate-300',
                'min': 0
            }),
        }
 

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['title', 'category', 'valuation', 'location', 'size', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-slate-300 rounded-xl px-3 py-2 text-sm',
                'placeholder': 'Asset Name'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border border-slate-300 rounded-xl px-3 py-2 text-sm'
            }),
            'valuation': forms.NumberInput(attrs={
                'class': 'w-full border border-slate-300 rounded-xl px-3 py-2 text-sm',
                'placeholder': 'Estimated Value in Ksh'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full border border-slate-300 rounded-xl px-3 py-2 text-sm',
                'placeholder': 'Location (if applicable)'
            }),
            'size': forms.TextInput(attrs={
                'class': 'w-full border border-slate-300 rounded-xl px-3 py-2 text-sm',
                'placeholder': 'Size / Metric'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border border-slate-300 rounded-xl px-3 py-2 text-sm',
                'rows': 3,
                'placeholder': 'Optional description'
            }),
        }

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['asset', 'member_name', 'share']
        widgets = {
            'asset': forms.HiddenInput(),  
            'member_name': forms.TextInput(attrs={
                'class': 'w-full border border-slate-300 rounded-xl px-3 py-2 text-sm',
                'placeholder': 'Full Name of Member'
            }),
            'share': forms.NumberInput(attrs={
                'class': 'w-full border border-slate-300 rounded-xl px-3 py-2 text-sm',
                'placeholder': 'Contribution / Share Value'
            }),
        }
