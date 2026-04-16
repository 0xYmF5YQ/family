from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    # Authentication
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    # Person management
    path("person/", views.person_list, name="family"),
    path("person/create/", views.person_create, name="person_create"),
    path("person/update/<int:pk>/", views.person_update, name="person_update"),
    path("person/delete/<int:pk>/", views.person_delete, name="person_delete"),
    # Event management
    path("event/", views.event_list, name="event_list"),
    path("event/create/", views.event_create, name="add_event"),
    path("event/update/<int:pk>/", views.event_update, name="event_update"),
    path("event/delete/<int:pk>/", views.event_delete, name="event_delete"),
    # Contributions
    path("contributions/", views.contributions, name="contributions"),
    path("contribution/create/", views.add_contribution, name="add_contribution"),
    # Assets
    path("asset/", views.asset_list, name="assets"),
    path("asset/update/<int:pk>/", views.asset_update, name="asset_update"),
    path("asset/delete/<int:pk>/", views.asset_delete, name="asset_delete"),
    path("asset/ownership/add/", views.add_asset_ownership, name="add_asset_ownership"),
    # API endpoints
    path(
        "recent-activities/", views.recent_activities_api, name="recent_activities_api"
    ),
    path("get-lineage/<int:pk>/", views.get_lineage, name="get_lineage"),
    path(
        "get-member-details/<int:id>/",
        views.get_member_details,
        name="get_member_details",
    ),
    path("assets/json/<int:id>/", views.asset_json, name="asset_json"),
    path("asset/<int:id>/owners/", views.add_owner, name="add_owner"),
]
