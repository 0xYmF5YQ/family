from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
#from .models import Parents, Children
from .models import Contribution, Event, Family, EventType, AssetCategory
from .models import Asset, Owner


class LoginForm(AuthenticationForm):
    name = forms.CharField(
        max_length=200,
        required=False,
        label="Full Name",
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )
    birth_year = forms.IntegerField(
        required=False,
        label="Year of Birth",
        widget=forms.NumberInput(attrs={'placeholder': 'Year of Birth'})
    )

    password = forms.CharField(
        required=False,
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        birth_year = cleaned_data.get('birth_year')
        password = cleaned_data.get('password')
        username = cleaned_data.get('username')  
       
        if (name and birth_year):
      
            return cleaned_data
        elif username and password:
            
            return cleaned_data
        else:
            raise forms.ValidationError(
                "Enter either Full Name + Birth Year."
            )
        return cleaned_data
      

"""class ParentForm(forms.ModelForm):
    class Meta:
        model = Parents
        fields = ['name', 'birth_date', 'parent'] 
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
                'placeholder': 'Full Name'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
                'type': 'date'
            }),
            'parent': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['parent'].queryset = Parents.objects.exclude(pk=self.instance.pk)
        else:
            self.fields['parent'].queryset = Parents.objects.all()

        self.fields['parent'].required = False 
        self.fields['parent'].label = "Parent (optional)"
class ChildForm(forms.ModelForm):
    class Meta:
        model = Children
        fields = ['name', 'birth_date', 'parent']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
                'placeholder': 'Enter full name'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
            }),
            'parent': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
            }),
        }
"""
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
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400'
            }),
            'type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400'
            }),
            'family_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400'
            }),
            'goal_amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
                'min': 0
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].queryset = EventType.objects.all()
        self.fields['type'].empty_label = "Select Event Type"



class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['event', 'family', 'member_name', 'amount']
        widgets = {
            'family': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400'
            }),
            'member_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
                'min': 0
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['family'].queryset = Family.objects.all()
        self.fields['family'].empty_label = "Select Family"



class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['title', 'category', 'valuation', 'location', 'size', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
                'placeholder': 'Asset Name'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400'
            }),
            'valuation': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
                'placeholder': 'Estimated Value in Ksh'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
                'placeholder': 'Location (if applicable)'
            }),
            'size': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
                'placeholder': 'Size / Metric'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
                'rows': 3,
                'placeholder': 'Optional description'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = AssetCategory.objects.all()
        self.fields['category'].empty_label = "Select a category"


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = [ 'member_name', 'share']
        widgets = {
            'asset': forms.HiddenInput(),  
            'member_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
                'placeholder': 'Full Name'
            }),
            'share': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400',
                'placeholder': 'Contribution / Share Value'
            }),
        }
