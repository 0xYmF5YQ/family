from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('parents/', views.parents, name='parents'),
    path('children/', views.children, name='children'),
    path('contributions/', views.contributions, name='contributions'),
    path('events/add/', views.add_event, name='add_event'),
    path('contributions/add/', views.add_contribution, name='add_contribution'),
    path('assets/', views.assets, name='assets'),
    path('assets/add/', views.add_asset, name='add_asset'),

    
]