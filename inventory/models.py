from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=64)
    supplier = models.CharField(max_length=64)
    weight = models.FloatField(default=0.0)

class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # product in the batch
    pur_date = models.DateField()  # purchased on
    exp_date = models.DateField()  # expires on
    init_qty = models.IntegerField(default=1)  # initial quantity
    curr_qty = models.IntegerField(default=1)  # current quantity
    tot_cost = models.FloatField(default=0.0)  # paid for the batch


class Events(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)  # batch it refers to
    ev_date = models.DateField()  # when it occurred
    ev_type = models.CharField(max_length=4)  # ADD, SUB
