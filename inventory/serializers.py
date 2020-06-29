from rest_framework import serializers
from .models import Product, Batch, Event


class ProductSerializer (serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ( 'id' , 'name' , 'supplier' , 'weight' )


class BatchSerializer (serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = (
            'id' , 'product' , 'pur_date' , 'exp_date',
            'init_qty', 'curr_qty', 'tot_cost'
        )
