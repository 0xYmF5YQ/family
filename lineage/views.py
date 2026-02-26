from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from .models import Person, Event, Contribution, Asset


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
