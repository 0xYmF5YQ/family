from django.shortcuts import render, redirect, get_object_or_404
from .models import Contribution, Asset, Event
from .forms import ContributionForm, EventForm, AssetForm, OwnerForm
from django.db.models import Sum, Q
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.timesince import timesince


@login_required
def home(request):
    return redirect('dashboard')


def dashboard(request):
    # total_assets count
    total_assets = Asset.objects.count()

    # Upcoming event
    upcoming_event = Event.objects.filter(date__gte=timezone.now()).order_by('date').first()

    # Recent contributions and assets
    recent_contribs = Contribution.objects.select_related('event').all().order_by('-contributed_at')
    recent_assets = Asset.objects.all().order_by('-created_at')

    combined_activities = []

    # Contributions
    for c in recent_contribs:
        combined_activities.append({
            'type': 'contribution',
            'name': c.member_name,
            'amount': c.amount,
            'event_name': c.event.title if c.event else '',
            'asset_name': '',
            'location': '',
            'created_at': c.contributed_at,
        })

    # Assets
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

    # Only placeholders for children and parents if used in future
    combined_activities.append({'type': 'child', 'amount': None, 'event_name': '', 'asset_name': '', 'location': ''})
    combined_activities.append({'type': 'parent', 'amount': None, 'event_name': '', 'asset_name': '', 'location': ''})

    # Get latest 5 activities
    recent_activities = combined_activities[:5]

    context = {
        'total_assets': total_assets,
        'upcoming_event': upcoming_event,
        'recent_activities': recent_activities,
    }

    return render(request, 'lineage/dashboard.html', context)


def recent_activities_api(request):
    page = int(request.GET.get('page', 1))
    per_page = 8

    recent_contribs = Contribution.objects.select_related('event').all().order_by('-contributed_at')
    recent_assets = Asset.objects.all().order_by('-created_at')

    combined_activities = []

    for c in recent_contribs:
        combined_activities.append({
            'type': 'contribution',
            'name': c.member_name,
            'amount': float(c.amount),
            'event_name': c.event.title if c.event else '',
            'asset_name': '',
            'location': '',
            'created_at': c.contributed_at,
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

    # Sorting all activities by creation time
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


def family(request):
    context = {}
    return render(request, 'lineage/family.html', context)


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
    assets_qs = Asset.objects.all().order_by('-created_at')
    total_valuation = assets_qs.aggregate(Sum('valuation'))['valuation__sum'] or 0
    form = AssetForm()
    owner_form = OwnerForm()

    context = {
        'assets': assets_qs,
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
