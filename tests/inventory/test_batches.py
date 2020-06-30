from django.urls import reverse
from rest_framework import status
import pytest

from inventory.models import Product


@pytest.mark.django_db
def test_product_create(api_client, sample_product):
    url = reverse('inventory:products')
    resp = api_client.post(url, sample_product)
    assert resp.status_code == status.HTTP_201_CREATED
    ret_prod = resp.json()
    assert ret_prod
    assert ret_prod['name'] == sample_product['name']
    assert Product.objects.count() == 1
    db_prod = Product.objects.get(pk=ret_prod['id'])
    assert db_prod.name == ret_prod['name']

@pytest.mark.django_db
@pytest.mark.xfail
def test_product_create_invalid_short_name(api_client, sample_product):
    url = reverse('inventory:products')
    sample_product['name'] = 'XY'
    resp = api_client.post(url, sample_product)
    assert resp.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
@pytest.mark.xfail
def test_product_create_invalid_weight(api_client, sample_product):
    url = reverse('inventory:products')
    sample_product['weight'] = 'XY'
    resp = api_client.post(url, sample_product)
    assert resp.status_code == status.HTTP_201_CREATED
