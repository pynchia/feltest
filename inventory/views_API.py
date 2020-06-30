from datetime import date

from django.db.models import Sum
from django.forms.models import model_to_dict

from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Batch, Event
from .serializers import ProductSerializer, BatchSerializer, EventSerializer


class ProductListCreate(generics.ListCreateAPIView):
    """
    GET all products
    Create a product (POST)
    """
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveAPIView):
    """
    GET the details of a specific product
    It includes the current inventory info (total and batch breakdown)
    """
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        batches = product.batch_set.order_by('exp_date')  # the batches where it appears
        batch_serializer = BatchSerializer(
            batches,
            many=True
        )
        curr_total_qty = batches.aggregate(Sum('curr_qty'))['curr_qty__sum']
        ret_obj = model_to_dict(product)  # basic product info
        ret_obj.update(
            curr_total_qty=curr_total_qty,  # add the total qty
            batches=batch_serializer.data  # and its batches
        )
        return Response(ret_obj)



class BatchListCreate(generics.ListCreateAPIView):
    """
    GET all batches
    Create a batch (POST)
    """
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

class BatchOverview(generics.ListAPIView):
    """
    GET an overview of all batches by freshness
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

    def patch(self, request, pk,*args, **kwargs):
        kwargs['partial'] = True
        batch = self.get_object()
        resp = self.partial_update(request, *args, **kwargs)
        event = Event.objects.create(
            batch=batch,
            ev_type=Event.TYPE_QTY,
            ev_info=f"From {batch.curr_qty} to {request.data['curr_qty']}"
        )
        return resp


class BatchHistory(generics.RetrieveAPIView):
    """
    GET the details of a specific product
    It includes the current inventory info (total and batch breakdown)
    """
    queryset = Batch.objects.all()

    def get(self, request, *args, **kwargs):
        batch = self.get_object()
        events = batch.event_set.order_by('ev_date')  # the events of this batch
        event_serializer = EventSerializer(
            events,
            many=True
        )
        ret_obj = model_to_dict(batch)  # basic batch info
        ret_obj.update(  # add its events
            events=event_serializer.data
        )
        return Response(ret_obj)
