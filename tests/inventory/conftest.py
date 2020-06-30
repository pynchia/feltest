import pytest

from inventory.models import Product, Batch, Event
from tests.inventory.sample_model_objects import sample_prod


@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()

@pytest.fixture
def create_product(db):
   def make_prod(**kwargs):
       return Product.objects.create(**kwargs)
   return make_prod

# @pytest.fixture
# def create_batch(db, create_product, api_client):
#    def make_batch(**kwargs):
#        prod = create_product(**sample_prod)
#        kwargs['product'] = prod
#        return Batch.objects.create(**kwargs)
#    return make_batch
