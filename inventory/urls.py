
from django.urls import path
from inventory import views


urlpatterns = [
    path('products/', views.Product.as_view(), name='products'),
    path('batches/', views.Batch.as_view(), name='batches'),
    path('events/', views.Event.as_view(), name='events'),
]
