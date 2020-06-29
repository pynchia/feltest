
from django.urls import path
from .views import IndexView
from .views_API import (
    ProductListCreate, ProductDetail,
    BatchListCreate,
)


app_name = 'inventory'
urlpatterns = [
    # path('', IndexView.as_view(), name='products'),
    path('products/', ProductListCreate.as_view(), name='products'),
    path('products/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('batches/', BatchListCreate.as_view(), name='batches'),
    # path('events/', views.EventView.as_view(), name='events'),
]
