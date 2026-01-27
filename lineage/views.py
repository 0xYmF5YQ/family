from django.shortcuts import render, redirect
from .models import Person, Contribution, Asset
from .forms import ParentForm, ChildForm
from django.db.models import Sum
from .models import Event, Contribution
from .forms import ContributionForm
from .forms import AssetForm
from django.contrib import messages
from lineage import models
from .models import Event, Contribution
from .forms import EventForm, ContributionForm
import datetime
from django.views.decorators.http import require_POST

def home(request):
    return redirect('parents')


def parents(request):
    context = {}
    return render(request, 'lineage/parents.html', context)


def children(request):
    context = {}
    return render(request, 'lineage/children.html', context)


def contributions(request):
    context = {}
    return render(request, 'lineage/contributions.html', context)


@require_POST
def add_event(request):
    form = EventForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('contributions')

@require_POST
def add_contribution(request):
    form = ContributionForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('contributions')


def assets(request):
    context = {}
    return render(request, 'lineage/assets.html', context)

@require_POST
def add_asset(request):
    form = AssetForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('assets')

