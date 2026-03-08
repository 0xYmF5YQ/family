from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("person/", views.person_list, name="family"),
    path("person/create/", views.person_create, name="person_create"),
    path("person/update/<int:pk>/", views.person_update, name="person_update"),
    path("person/delete/<int:pk>/", views.person_delete, name="person_delete"),
    path("event/", views.event_list, name="event_list"),
    path("event/create/", views.event_create, name="event_create"),
    path("event/update/<int:pk>/", views.event_update, name="event_update"),
    path("event/delete/<int:pk>/", views.event_delete, name="event_delete"),
    path("contribution/create/", views.contribution_create, name="contributions"),
    path("asset/", views.asset_list, name="asset_list"),
    path("asset/create/", views.asset_create, name="assets"),
    path("asset/update/<int:pk>/", views.asset_update, name="logout"),
    path("asset/delete/<int:pk>/", views.asset_delete, name="asset_delete"),
    path("asset/ownership/add/", views.add_asset_ownership, name="add_asset_ownership"),
    path(
        "recent-activities/", views.recent_activities_api, name="recent_activities_api"
    ),
    path("get-lineage/<int:pk>/", views.get_lineage, name="get_lineage"),
    
]
