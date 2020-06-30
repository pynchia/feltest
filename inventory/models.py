
from django.db import models
from django.core.validators import MinLengthValidator


class Product(models.Model):
    NAME_MIN_LEN = 3
    name = models.CharField(max_length=64,
                            validators=[MinLengthValidator(NAME_MIN_LEN)])  # Product name
    weight = models.FloatField(default=0.0)  # in Kg
    # valid = models.BooleanField(default=True)


class Batch(models.Model):
    SUPPLIER_MIN_LEN = 4

    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # product in the batch
    supplier = models.CharField(max_length=64,
                                validators=[MinLengthValidator(SUPPLIER_MIN_LEN)])  # Bought from
    pur_date = models.DateField(auto_now_add=True)  # purchased on
    exp_date = models.DateField()  # expires on
    init_qty = models.IntegerField()  # initial quantity
    curr_qty = models.IntegerField(default=1)  # current quantity
    tot_cost = models.FloatField()  # paid for the batch


class Event(models.Model):
    TYPE_QTY = 'QTY'
    EV_TYPES = [
        (TYPE_QTY, 'Quantity'),
    ]
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)  # batch it refers to
    ev_date = models.DateTimeField(auto_now_add=True)  # when it occurred
    ev_type = models.CharField(choices=EV_TYPES, max_length=8)  # what happened
    ev_info = models.CharField(max_length=64)  # further info
