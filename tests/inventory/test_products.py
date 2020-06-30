
from django.urls import reverse
from rest_framework import status
import pytest

from inventory.models import Product
from tests.inventory.utils import add_many_products, add_many_batches


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
    sample_product1 = {"name": "Orange", "weight": 0.2}
    sample_product2 = {"name": "Banana", "weight": 5.0}
    sample_products = [sample_product1, sample_product2]
    add_many_products(api_client, sample_products)

    # retrieve all products
    url = reverse('inventory:products')
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    products = resp.json()
    # check they are all there
    assert len(products) == 2
    # and are returned ordered by name
    for prod, sample in zip(products,
                            sorted(sample_products, key=lambda p: p['name'])):
        assert prod['name'] == sample['name']

@pytest.mark.django_db
def test_product_get_one(api_client, sample_product, create_product):
    product = create_product(**sample_product)
    sample_batch1 = {
        "supplier": "ACME",
        "exp_date": "2020-07-21",
        "init_qty": 1000,
        "tot_cost": 2000
    }
    sample_batch1['product'] = product.id
    sample_batch2 = {
        "supplier": "Pune Ltd",
        "exp_date": "2020-07-01",
        "init_qty": 500,
        "tot_cost": 800
    }
    sample_batch2['product'] = product.id
    sample_batches = [sample_batch1, sample_batch2]
    add_many_batches(api_client, sample_batches)

    # retrieve one product
    url = reverse('inventory:product_detail', args=(product.id,))
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    product = resp.json()
    # check the batches it belongs to are all present
    prod_batches = product['batches']
    assert len(prod_batches) == 2
    # and are ordered by exp_date
    for prod, sample in zip(prod_batches,
                            sorted(sample_batches, key=lambda p: p['exp_date'])):
        assert prod['exp_date'] == sample['exp_date']
        assert prod['supplier'] == sample['supplier']

@pytest.mark.django_db
def test_product_update_patch_disallowed(api_client, sample_product, create_product):
    product = create_product(**sample_product)
    url = reverse('inventory:product_detail', args=(product.id,))
    resp = api_client.put(url, sample_product, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    resp = api_client.patch(url, sample_product, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
