
from django.urls import reverse
from rest_framework import status
import pytest

from inventory.models import Product


@pytest.mark.django_db
def test_product_create(api_client, sample_product):
    url = reverse('inventory:products')
    resp = api_client.post(url, sample_product, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    ret_prod = resp.json()
    assert ret_prod['name'] == sample_product['name']
    assert Product.objects.count() == 1
    db_prod = Product.objects.get(pk=ret_prod['id'])
    assert db_prod.name == ret_prod['name']

@pytest.mark.django_db
def test_product_create_invalid_short_name(api_client, sample_product):
    url = reverse('inventory:products')
    sample_product['name'] = 'XY'
    resp = api_client.post(url, sample_product, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_product_create_invalid_weight(api_client, sample_product):
    url = reverse('inventory:products')
    sample_product['weight'] = 'XY'
    resp = api_client.post(url, sample_product, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_product_get_all(api_client):
    url = reverse('inventory:products')
    sample_product1 = {"name": "Orange", "weight": 0.2}
    sample_product2 = {"name": "Banana", "weight": 5.0}
    sample_products = [sample_product1, sample_product2]
    add_many_products(api_client, sample_products)
    # retrieve all products
    products = api_client.get(url).json()
    # check they are all there
    # and are returned ordered by name
    for prod, sample in zip(products,
                            sorted(sample_products, key=lambda p: p['name'])):
        assert prod['name'] == sample['name']


# Utils

def add_many_products(api_client, products):
    url = reverse('inventory:products')
    for prod in products:
        resp = api_client.post(url, prod, format='json')
        assert resp.status_code == status.HTTP_201_CREATED
        ret_prod = resp.json()
        assert ret_prod['name'] == prod['name']
