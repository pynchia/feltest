
from django.urls import path
from inventory import views


urlpatterns = [
    path('products/', Product.as_view(), name='products'),
    path('batches/', Batch.as_view(), name='batches'),
    path('events/', Event.as_view(), name='events'),
]
