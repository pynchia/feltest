
from django.contrib import admin
from django.urls import include, path

from inventory.views import IndexView


urlpatterns = [
    path('inventory/api/v1.0/', include('inventory.urls')),
    path('', IndexView.as_view(), name='overview'),  # use for demo only
    path('admin/', admin.site.urls),
]
