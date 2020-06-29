
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('inventory/api/v1.0/', include('inventory.urls')),
    path('admin/', admin.site.urls),
]
