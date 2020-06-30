from django.urls import reverse
import pytest

from inventory.models import Product
from tests.inventory.sample_model_objects import sample_prod


@pytest.mark.django_db
def test_product_create(api_client):
    url = reverse('inventory:products')
    ret_prod = api_client.post(url, sample_prod).json()
    assert ret_prod['name'] == sample_prod['name']
    assert Product.objects.count() == 1
    db_prod = Product.objects.get(pk=ret_prod['id'])
    assert db_prod.name == ret_prod['name']
