from django.urls import reverse
from rest_framework import status
import pytest

from inventory.models import Product, Batch


@pytest.mark.django_db
def test_batch_create(api_client, sample_batch):
    url = reverse('inventory:batches')
    resp = api_client.post(url, sample_batch, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    ret_batch = resp.json()
    assert ret_batch['id'] == sample_batch['product']
    assert Product.objects.count() == 1
    assert Batch.objects.count() == 1
    db_prod = Batch.objects.get(pk=ret_batch['id'])
    assert db_prod.supplier == ret_batch['supplier']
    # etc. for the other fields

@pytest.mark.django_db
def test_batch_create_invalid_short_supplier(api_client, sample_batch):
    url = reverse('inventory:batches')
    sample_batch['supplier'] = 'XYZ'
    resp = api_client.post(url, sample_batch, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_product_create_invalid_qty(api_client, sample_batch):
    url = reverse('inventory:batches')
    sample_batch['init_qty'] = 'XY'
    resp = api_client.post(url, sample_batch, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
