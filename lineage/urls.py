from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
  
    path('', auth_views.login_view, name='login'),


    path('dashboard/', views.dashboard, name='dashboard'),
    #path('dashboard/activities/json/<int:page>/', views.dashboard_activities_json, name='dashboard_activities_json'),
    path('api/recent-activities/', views.recent_activities_api, name='recent_activities_api'),

    path('parents/', views.parent, name='parents'),
    path('parents/<int:pk>/', views.parent_detail, name='parent_detail'),

    path('children/', views.children, name='children'),
    path('children/<int:pk>/', views.child_detail, name='child_detail'),

    path('contributions/', views.contributions, name='contributions'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/json/<int:event_id>/', views.event_detail_json, name='event_detail_json'),
    path('contributions/add/', views.add_contribution, name='add_contribution'),

    path('assets/', views.assets, name='assets'),
    path('assets/add/', views.add_asset, name='add_asset'),
    path('assets/json/<int:asset_id>/', views.asset_detail_json, name='asset_detail_json'),
    path('assets/<int:asset_id>/add_owner/', views.add_owner, name='add_owner'),

    path('login/', auth_views.login_view, name='login'),
    #path('signup/', auth_views.signup_view, name='signup'),
    path('logout/', auth_views.logout_view, name='logout'),

    
]