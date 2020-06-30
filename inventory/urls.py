
from django.urls import path
from .views_API import (
    ProductListCreate, ProductDetail,
    BatchListCreate, BatchDetail, BatchHistory,
)


app_name = 'inventory'
urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='products'),
    path('products/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('batches/', BatchListCreate.as_view(), name='batches'),
    path('batches/<int:pk>', BatchDetail.as_view(), name='batch_detail'),
    path('batches/<int:pk>/history', BatchHistory.as_view(), name='batch_history'),
]
