import pytest

from inventory.models import Product, Batch, Event
from tests.inventory.sample_model_objects import sample_prod, sample_bat


@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()

@pytest.fixture
def sample_product():
   return sample_prod.copy()

@pytest.fixture
def create_product(db):
   def make_prod(**kwargs):
       return Product.objects.create(**kwargs)
   return make_prod

@pytest.fixture
def sample_batch(db, create_product, sample_product):
   prod = create_product(**sample_prod)
   ret_batch = sample_bat.copy()
   ret_batch['product'] = prod.id
   return ret_batch
