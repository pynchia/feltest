# from django.shortcuts import render
# from django.http import HttpResponse

from django.views import generic
from datetime import date

from .models import Batch, Event, Product


# Create your views here.


class IndexView(generic.ListView):
    template_name = 'inventory/index.html'
    context_object_name = 'batches'

    def get_queryset(self):
        """Return three sets of batches, by exp_date:
        Fresh, Expirying today, Expired
        """
        today = date.today()
        return {
            "fresh": Batch.objects.filter(exp_date__gt=today).order_by('exp_date'),
            "today": Batch.objects.filter(exp_date=today).order_by('pur_date'),
            "expired": Batch.objects.filter(exp_date__lt=today).order_by('exp_date'),
        }
