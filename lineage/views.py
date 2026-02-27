from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.utils import timezone
from .models import Person, Event, Contribution, Asset
from .forms import (
    AssetForm,
    AssetOwnershipForm,
    ContributionForm,
    EventForm,
    PersonForm,
)
from django.core.paginator import Paginator
from django.utils.timesince import timesince
from django.http import JsonResponse


def dashboard(request):
    total_parents = (
        Person.objects.filter(
            Q(children_from_father__isnull=False)
            | Q(children_from_mother__isnull=False)
        )
        .distinct()
        .count()
    )

    total_children = Person.objects.filter(
        Q(father__isnull=False) | Q(mother__isnull=False)
    ).count()

    total_assets = Asset.objects.count()

    upcoming_event = (
        Event.objects.filter(date__gte=timezone.now().date(), is_active=True)
        .order_by("date")
        .first()
    )

    # Recent activities (latest 5)
    contributions = Contribution.objects.select_related("member", "event").order_by(
        "-contributed_at"
    )[:5]
    assets = Asset.objects.order_by("-created_at")[:5]
    children = Person.objects.filter(
        Q(father__isnull=False) | Q(mother__isnull=False)
    ).order_by("-id")[:5]

    recent_activities = []

    for c in contributions:
        recent_activities.append(
            {
                "type": "contribution",
                "name": str(c.member),
                "amount": c.amount,
                "event_name": c.event.title,
                "created_at": c.contributed_at,
            }
        )

    for a in assets:
        recent_activities.append(
            {
                "type": "asset",
                "asset_name": a.title,
                "location": a.location,
                "created_at": a.created_at,
            }
        )

    for child in children:
        recent_activities.append(
            {
                "type": "child",
                "name": str(child),
                "location": str(child.father or child.mother),
                "created_at": child.id,  # fallback ordering
            }
        )

    recent_activities = sorted(
        recent_activities, key=lambda x: x["created_at"], reverse=True
    )[:5]

    context = {
        "total_parents": total_parents,
        "total_children": total_children,
        "total_assets": total_assets,
        "upcoming_event": upcoming_event,
        "recent_activities": recent_activities,
    }

    return render(request, "lineage/dashboard.html", context)


def person_list(request):
    persons = Person.objects.all()
    form = PersonForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("family")
    return render(request, "lineage/family.html", {"persons": persons, "form": form})


def person_create(request):
    form = PersonForm(request.POST or None, request.FILES or None)

    return render(request, "lineage/form.html", {"form": form})


def person_update(request, pk):
    person = get_object_or_404(Person, pk=pk)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if form.is_valid():
        form.save()
        return redirect("person_list")

    return render(request, "lineage/form.html", {"form": form})


def person_delete(request, pk):
    person = get_object_or_404(Person, pk=pk)
    person.delete()
    return redirect("person_list")


def event_list(request):
    events = Event.objects.all()
    return render(request, "lineage/event_list.html", {"events": events})


def event_create(request):
    form = EventForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("event_list")

    return render(request, "lineage/form.html", {"form": form})


def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect("event_list")

    return render(request, "lineage/form.html", {"form": form})


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect("event_list")


def contribution_create(request):
    form = ContributionForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("dashboard")

    return render(request, "lineage/form.html", {"form": form})


def asset_list(request):
    assets = Asset.objects.all()
    return render(request, "lineage/asset_list.html", {"assets": assets})


def asset_create(request):
    form = AssetForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("asset_list")

    return render(request, "lineage/form.html", {"form": form})


def asset_update(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    form = AssetForm(request.POST or None, instance=asset)

    if form.is_valid():
        form.save()
        return redirect("asset_list")

    return render(request, "lineage/form.html", {"form": form})


def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    asset.delete()
    return redirect("asset_list")


def add_asset_ownership(request):
    form = AssetOwnershipForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("asset_list")

    return render(request, "lineage/form.html", {"form": form})


def recent_activities_api(request):
    page_number = request.GET.get("page", 1)

    contributions = Contribution.objects.select_related("member", "event").order_by(
        "-contributed_at"
    )

    paginator = Paginator(contributions, 5)
    page_obj = paginator.get_page(page_number)

    activities = []

    for c in page_obj:
        activities.append(
            {
                "type": "contribution",
                "member_name": str(c.member),
                "amount": f"{c.amount:,.0f}",
                "event_name": c.event.title,
                "time_since": timesince(c.contributed_at),
            }
        )

    return JsonResponse({"activities": activities})
