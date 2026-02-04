from django.shortcuts import render, redirect, get_object_or_404
from .models import Parents, Children, Contribution, Asset,Event
from .forms import ParentForm, ChildForm, ContributionForm, EventForm, AssetForm, OwnerForm
from django.db.models import Sum
from django.contrib import messages
from lineage import models
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def home(request):
    return redirect('parents')


def parent(request):
    all_parents = Parents.objects.all().order_by('-id')

    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Parent added successfully!")
            return redirect('parents') 
    else:
        form = ParentForm()

    context = {
        'all_parents': all_parents,
        'form': form,
    }
    return render(request, 'lineage/parents.html', context)

def parent_detail(request, pk):
    parent = get_object_or_404(Parents, pk=pk)
    children = parent.children.all()
    

    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = parent  
            child.save()
            messages.success(request, "Child added successfully!")
            return redirect('parent_detail', pk=parent.pk)
    else:
        form = ChildForm()

    return render(request, 'lineage/parent_detail.html', {
        'parent': parent,
        'children': children,
        'form': form,
        
    })




def children(request):
    all_children = Children.objects.select_related('parent').all().order_by('name')
    
    return render(request, 'lineage/children.html', {
        'children': all_children
    })

def child_detail(request, pk):
   
    child = get_object_or_404(Children, pk=pk)
    
   
    siblings = []
    if child.parent:
        siblings = Children.objects.filter(parent=child.parent).exclude(id=child.id)
    
    return render(request, 'lineage/child_detail.html', {
        'child': child,
        'parent': child.parent,
        'siblings': siblings,
        
    })



def contributions(request):
   
    today = timezone.now().date()
    
    active_events = Event.objects.filter(date__gte=today).order_by('date')
    archived_events = Event.objects.filter(date__lt=today).order_by('-date')
    
    event_form = EventForm()
    contribution_form = ContributionForm()

    context = {
        'events': active_events,           
        'archived_events': archived_events, 
        'event_form': event_form,
        'contribution_form': contribution_form,
    }
    return render(request, 'lineage/contributions.html', context)

@require_POST
def add_event(request):
    form = EventForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Event added successfully!")
    return redirect('contributions')

@require_POST
def add_contribution(request):
    form = ContributionForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Contribution added!")
    else:
        
        print(form.errors) 
    return redirect('contributions')

def event_detail_json(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    contributions_qs = event.contributions.all().order_by('-created_at').values(
        'member_name', 'amount', 'created_at'
    )
    
    data = {
        'title': event.title,
        'family_name': event.family_name,
        'goal_amount': float(event.goal_amount),
        'total_raised': float(event.total_contributed), 
        'contributions': list(contributions_qs),
    }
    return JsonResponse(data)


def assets(request):
    assets = Asset.objects.all().order_by('-created_at')
    total_valuation = assets.aggregate(Sum('valuation'))['valuation__sum'] or 0
    form = AssetForm()
    owner_form = OwnerForm()
    
    context = {
        'assets': assets,
        'total_valuation': total_valuation,
        'form': form,
        'owner_form': owner_form,
    }
    return render(request, 'lineage/assets.html', context)

@require_POST
def add_asset(request):
    form = AssetForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Asset added successfully!")
    return redirect('assets')

def asset_detail_json(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    owners = asset.owners.all().order_by('-created_at')
    
    data = {
        'title': asset.title,
        'category': asset.get_category_display(),
        'valuation': float(asset.valuation),
        'owners': [
            {
                'member_name': o.member_name,
                'share': o.share,
                'created_at': o.created_at.strftime('%b %d, %Y')
            } for o in owners
        ]
    }
    return JsonResponse(data)


def add_owner(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    
    if request.method == "POST":
        form = OwnerForm(request.POST)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.asset = asset
            owner.save()
            messages.success(request, "Owner added successfully!")
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'member_name': owner.member_name,
                    'share': owner.share,
                    'created_at': owner.created_at.strftime('%b %d, %Y')
                })
            return redirect('assets')
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        
    return redirect('assets')
