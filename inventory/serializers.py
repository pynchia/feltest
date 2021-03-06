
from rest_framework import serializers
from .models import Product, Batch, Event


class ProductSerializer (serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ( 'id' , 'name' , 'weight' )


class BatchSerializer (serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = (
            'id' , 'product' , 'supplier', 'pur_date' , 'exp_date',
            'init_qty', 'curr_qty', 'tot_cost'
        )

    def create(self, validated_data):
        return Batch.objects.create(
            **validated_data,
            curr_qty=validated_data['init_qty']
        )

    def update(self, instance, validated_data):
        curr_qty = validated_data.get('curr_qty')
        if curr_qty is not None:
            instance.curr_qty = curr_qty
            instance.save()
        return instance


class EventSerializer (serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id' , 'batch' , 'ev_date' , 'ev_type',
            'ev_info',
        )
