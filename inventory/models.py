from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=64)  # Product name
    supplier = models.CharField(max_length=64)  # Bought from
    weight = models.FloatField(default=0.0)  # in Kg
    # valid = models.BooleanField(default=True)


class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # product in the batch
    pur_date = models.DateField(auto_now_add=True)  # purchased on
    exp_date = models.DateField()  # expires on
    init_qty = models.IntegerField(default=1)  # initial quantity
    curr_qty = models.IntegerField(default=1)  # current quantity
    tot_cost = models.FloatField(default=0.0)  # paid for the batch


class Event(models.Model):
    EV_TYPES = [
        ('QTY', 'Quantity'),
    ]
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)  # batch it refers to
    ev_date = models.DateField(auto_now_add=True)  # when it occurred
    ev_type = models.CharField(choices=EV_TYPES, max_length=8)  # what happened
