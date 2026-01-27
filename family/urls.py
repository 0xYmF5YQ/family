from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect



urlpatterns = [
    path('', include('lineage.urls')),
    path('admin/', admin.site.urls),
    path('lineage/', include('lineage.urls')),
]
