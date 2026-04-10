from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.utils import timezone
from .models import AssetOwnership, Person, Event, Contribution, Asset
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

    context = {
        "total_parents": total_parents,
        "total_children": total_children,
        "total_assets": total_assets,
        "upcoming_event": upcoming_event,
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

    return render(request, "lineage/profile.html", {"form": form})


def person_delete(request, pk):
    person = get_object_or_404(Person, pk=pk)
    person.delete()
    return redirect("person_list")


def event_list(request):
    events = Event.objects.all()
    return render(request, "lineage/event.html", {"events": events})


def event_create(request):

    return render(request, "lineage/contributions.html")


def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form1 = EventForm(request.POST or None, instance=event)

    if form1.is_valid():
        form1.save()
        return redirect("event_list")

    return render(request, "lineage/form.html", {"form1": form1})


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect("event_list")


def contributions(request):
    event_form = EventForm()
    return render(request, "lineage/contributions.html", {"event_form": event_form})


def event_create(request):
    event_form = EventForm(request.POST or None)

    if request.method == "POST" and event_form.is_valid():
        event_form.save()
        return redirect("contributions")  # go back to the page with the modal

    return render(request, "lineage/contributions.html", {"event_form": event_form})


# this is dummy for now
def add_contribution(request):
    form = ContributionForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("contributions")

    return render(request, "lineage/form.html", {"form": form})


def asset_list(request):
    assets = Asset.objects.all()
    total_valuation = sum(a.valuation for a in assets)
    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("assets")
        else:
            print(form.errors)
    else:
        form = AssetForm()

    return render(
        request,
        "lineage/assets.html",
        {
            "assets": assets,
            "form": form,
            "total_valuation": total_valuation,
        },
    )


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


def get_lineage(request, pk):
    person = get_object_or_404(Person, pk=pk)
    father = person.father
    grandfather = person.get_father_ancestor(2)
    great_grandfather = person.get_father_ancestor(3)

    children = person.get_children()
    offspring_summary = (
        ", ".join([f"{child.first_name} {child.last_name}" for child in children])
        if children
        else None
    )

    return JsonResponse(
        {
            "grandfather": str(grandfather) if grandfather else None,
            "great_grandfather": str(great_grandfather) if great_grandfather else None,
            "offspring_summary": offspring_summary,
            "father": str(father) if father else None,
        }
    )


def get_member_details(request, id):
    person = get_object_or_404(Person, id=id)

    data = {
        "id": person.id,
        "first_name": person.first_name,
        "last_name": person.last_name,
        "birth_date": (
            person.birth_date.strftime("%Y-%m-%d") if person.birth_date else None
        ),
        "age": person.get_age(),
        "gender": person.get_gender_display() if person.gender else None,
        "status": person.get_status_display(),
        "job_status": person.get_job_status_display(),
        "disability_status": person.get_disability_status_display(),
        "father": str(person.father) if person.father else None,
        "mother": str(person.mother) if person.mother else None,
        "spouse": str(person.spouse) if person.spouse else None,
        "family_root": (
            str(person.get_family_root()) if person.get_family_root() else None
        ),
        "great_grandfather": (
            str(person.great_grandfather) if person.great_grandfather else None
        ),
        "children": [str(child) for child in person.get_children()],
        "siblings": [str(s) for s in person.get_siblings()],
        "grandchildren": [str(gc) for gc in person.get_grandchildren()],
        "great_grandchildren": [str(ggc) for ggc in person.get_great_grandchildren()],
        "photo_url": person.photo.url if person.photo else None,
    }

    return JsonResponse(data)
