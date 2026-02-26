from django import forms
from .models import (
    Person,
    EventType,
    Event,
    Contribution,
    Asset,
    AssetOwnership,
)


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "status",
            "job_status",
            "disability_status",
            "gender",
            "father",
            "mother",
            "spouse",
            "photo",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        father = cleaned_data.get("father")
        mother = cleaned_data.get("mother")

        if father and father.gender != "M":
            raise forms.ValidationError("Father must be male.")

        if mother and mother.gender != "F":
            raise forms.ValidationError("Mother must be female.")

        return cleaned_data


class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = ["name"]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "type",
            "family_name",
            "location",
            "date",
            "goal_amount",
            "is_active",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_date(self):
        event_date = self.cleaned_data.get("date")
        if event_date and event_date.year < 1900:
            raise forms.ValidationError("Invalid event date.")
        return event_date


class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = [
            "event",
            "member",
            "amount",
        ]

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount and amount <= 0:
            raise forms.ValidationError("Contribution amount must be positive.")
        return amount


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            "title",
            "status",
            "valuation",
            "location",
            "size",
            "description",
            "owners",
        ]


class AssetOwnershipForm(forms.ModelForm):
    class Meta:
        model = AssetOwnership
        fields = [
            "asset",
            "owner",
            "share",
        ]

    def clean_share(self):
        share = self.cleaned_data.get("share")
        if share and (share <= 0 or share > 100):
            raise forms.ValidationError(
                "Ownership share must be between 0 and 100 percent."
            )
        return share
