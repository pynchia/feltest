from datetime import date

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Batch, Event
from .serializers import ProductSerializer, BatchSerializer


class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BatchListCreate(generics.ListCreateAPIView):
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

    # def post(self, request, format=None):
    #     serializer = BatchSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.validated_data['curr_qty'] = serializer.validated_data['init_qty']
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BatchDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
