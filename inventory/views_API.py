from datetime import date

from django.db.models import Sum

from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Batch, Event
from .serializers import ProductSerializer, BatchSerializer


class ProductListCreate(generics.ListCreateAPIView):
    """
    GET all products
    Create a product (POST)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveAPIView):
    """
    GET the details of a specific product
    It includes the current inventory info (total and batch breakdown)
    """
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        batches = product.batch_set.all()  # the batches where it appears
        curr_total_qty = batches.aggregate(Sum('curr_qty'))['curr_qty__sum']
        batch_serializer = BatchSerializer(
            product.batch_set.all().order_by('exp_date'),
            many=True
        )
        return Response({
            "name": product.name,
            "supplier": product.supplier,
            "weight": product.weight,
            "curr_total_qty": curr_total_qty,
            "batches": batch_serializer.data
        })


class BatchListCreate(generics.ListCreateAPIView):
    """
    GET all batches (as an overview by freshness)
    Create a batch (POST)
    """
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    def get(self, request, *args, **kwargs):
        """
        Return all batches, grouped by freshness
        """
        today = date.today()
        fresh_serializer = BatchSerializer(
            Batch.objects.filter(exp_date__gt=today).order_by('exp_date'),
            many=True
        )
        today_serializer = BatchSerializer(
            Batch.objects.filter(exp_date=today).order_by('pur_date'),
            many=True
        )
        expired_serializer = BatchSerializer(
            Batch.objects.filter(exp_date__lt=today).order_by('exp_date'),
            many=True
        )
        return Response({
            "fresh": fresh_serializer.data,
            "today": today_serializer.data,
            "expired": expired_serializer.data,
        })


class BatchDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    """
    GET the details of a specific batch
    Modify a batch (PATCH only, as only the curr_qty can be modified)
    """
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer  

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.partial_update(request, *args, **kwargs)
