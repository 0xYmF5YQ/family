from django.shortcuts import render, redirect, get_object_or_404
from .models import Parents, Children, Contribution, Asset, Event
from .forms import ParentForm, ChildForm, ContributionForm, EventForm, AssetForm, OwnerForm
from django.db.models import Sum
from django.contrib import messages
from lineage import models
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter
from django.core.paginator import Paginator
from django.utils.timesince import timesince

@login_required
def login(request):
    return redirect('dashboard')


def dashboard(request):
    total_parents = Parents.objects.count()
    total_children = Children.objects.count()
    total_assets = Asset.objects.count()
    upcoming_event = Event.objects.filter(date__gte=timezone.now()).order_by('date').first()

    recent_contribs = Contribution.objects.select_related('event').all().order_by('-created_at')
    recent_assets = Asset.objects.all().order_by('-created_at')
    recent_children = Children.objects.select_related('parent').all().order_by('-created_at')
    recent_parents = Parents.objects.all().order_by('-created_at')

    combined_activities = []
    for c in recent_contribs:
        combined_activities.append({
            'type': 'contribution',
            'name': c.member_name,
            'amount': c.amount,
            'event_name': c.event.title if c.event else '',
            'asset_name': '',
            'location': '',
            'created_at': c.created_at,
        })
    for a in recent_assets:
        combined_activities.append({
            'type': 'asset',
            'name': '',
            'amount': None,
            'event_name': '',
            'asset_name': a.title,
            'location': a.location or 'Unknown',
            'created_at': a.created_at,
        })
    for ch in recent_children:
        combined_activities.append({
            'type': 'child',
            'name': ch.name,
            'amount': None,
            'event_name': '',
            'asset_name': '',
            'location': ch.parent.name if ch.parent else 'Unknown',
            'created_at': ch.created_at,
        })
    for p in recent_parents:
        combined_activities.append({
            'type': 'parent',
            'name': p.name,
            'amount': None,
            'event_name': '',
            'asset_name': '',
            'location': '',
            'created_at': p.created_at,
        })

    combined_activities.sort(key=lambda x: x['created_at'], reverse=True)

    recent_activities = combined_activities[:5]

    context = {
        'total_parents': total_parents,
        'total_children': total_children,
        'total_assets': total_assets,
        'upcoming_event': upcoming_event,
        'recent_activities': recent_activities,
    }

    return render(request, 'lineage/dashboard.html', context)


def recent_activities_api(request):
    page = int(request.GET.get('page', 1))
    per_page = 8
    recent_contribs = Contribution.objects.select_related('event').all().order_by('-created_at')
    recent_assets = Asset.objects.all().order_by('-created_at')
    recent_children = Children.objects.select_related('parent').all().order_by('-created_at')
    recent_parents = Parents.objects.order_by('-created_at')

    combined_activities = []

    for c in recent_contribs:
        combined_activities.append({
            'type': 'contribution',
            'name': c.member_name,
            'amount': float(c.amount),
            'event_name': c.event.title if c.event else '',
            'asset_name': '',
            'location': '',
            'created_at': c.created_at,
        })

    for a in recent_assets:
        combined_activities.append({
            'type': 'asset',
            'name': '',
            'amount': None,
            'event_name': '',
            'asset_name': a.title,
            'location': a.location or 'Unknown',
            'created_at': a.created_at,
        })

    for ch in recent_children:
        combined_activities.append({
            'type': 'child',
            'name': ch.name,
            'amount': None,
            'event_name': '',
            'asset_name': '',
            'location': ch.parent.name if ch.parent else 'Unknown',
            'created_at': ch.created_at,
        })
    for p in recent_parents:
        combined_activities.append({
            'type': 'parent',
            'name': p.name,
            'amount': None,
            'event_name': '',
            'asset_name': '',
            'location': '',
            'created_at': p.created_at,
        })
   
    combined_activities.sort(key=lambda x: x['created_at'], reverse=True)

   
    start = (page - 1) * per_page
    end = start + per_page
    page_activities = combined_activities[start:end]
    has_next = len(combined_activities) > end

   
    activity_list = []
    for act in page_activities:
        activity_list.append({
            'type': act['type'],
            'name': act['name'],
            'amount': act['amount'],
            'event_name': act['event_name'],
            'asset_name': act['asset_name'],
            'location': act['location'],
            'time_since': timesince(act['created_at']),
        })

    return JsonResponse({
        'activities': activity_list,
        'has_next': has_next,
    })



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
        'member_name', 
        'amount', 
        'created_at',
        'family__name'  
    )

    contributions = []
    for c in contributions_qs:
        contributions.append({
            "member_name": c['member_name'],
            "family_name": c['family__name'] or "",  
            "amount": float(c['amount']),
            "created_at": c['created_at'].isoformat()
        })
    
    data = {
        'title': event.title,
        'family_name': event.family_name,
        'goal_amount': float(event.goal_amount),
        'total_raised': float(event.total_contributed), 
        'contributions': contributions,
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
        'category': asset.category.name if asset.category else None,
        'valuation': float(asset.valuation),
        'owners': [
            {
                'member_name': o.member_name,
                'share': float(o.share),
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
