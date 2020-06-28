
from django.urls import path
from . import views

app_name = 'inventory'
urlpatterns = [
    path('', views.IndexView.as_view(), name='products'),
    # path('products/', views.ProductView.as_view(), name='products'),
    # path('batches/', views.BatchView.as_view(), name='batches'),
    # path('events/', views.EventView.as_view(), name='events'),
]
