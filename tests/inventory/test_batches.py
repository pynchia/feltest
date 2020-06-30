from datetime import date, timedelta
from django.urls import reverse
from rest_framework import status
import pytest

from inventory.models import Product, Batch
from tests.inventory.utils import add_many_products, add_many_batches


@pytest.mark.django_db
def test_batch_create(api_client, sample_batch):
    url = reverse('inventory:batches')
    resp = api_client.post(url, sample_batch, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    ret_batch = resp.json()
    assert ret_batch['id'] == sample_batch['product']
    # check in the DB
    assert Product.objects.count() == 1
    assert Batch.objects.count() == 1
    db_prod = Batch.objects.get(pk=ret_batch['id'])
    assert db_prod.supplier == ret_batch['supplier']
    # etc. for the remaining fields
    # now check by retrieving it from the endpoint
    url = reverse('inventory:batch_detail', args=(ret_batch['id'],))
    resp = api_client.get(url, format='json')
    assert resp.status_code == status.HTTP_200_OK
    batch = resp.json()
    assert batch['pur_date'] == str(date.today())
    assert batch['curr_qty'] == sample_batch['init_qty']
    del batch['id'], batch['pur_date'], batch['curr_qty']
    assert batch == sample_batch

@pytest.mark.django_db
def test_batch_create_invalid_short_supplier(api_client, sample_batch):
    url = reverse('inventory:batches')
    sample_batch['supplier'] = 'XYZ'
    resp = api_client.post(url, sample_batch, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_batch_create_invalid_qty(api_client, sample_batch):
    url = reverse('inventory:batches')
    sample_batch['init_qty'] = 'XY'
    resp = api_client.post(url, sample_batch, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_batches_overview(api_client, create_product):
    sample_prod1 = {"name": "Orange", "weight": "0.2"}
    sample_prod2 = {"name": "Banana", "weight": "2.2"}
    sample_prod3 = {"name": "Melon", "weight": "3.1"}
    created_prods = [
        create_product(prod) for prod in (sample_prod1, sample_prod2, sample_prod3)
    ]
    sample_batch_fresh = {
        "product": created_prods[0].id,
        "supplier": "ACME",
        "exp_date": "2020-07-21",
        "init_qty": 1000,
        "tot_cost": 2000.0
    }
    sample_batch_exp_today1 = {
        "product": created_prods[1].id,
        "supplier": "Pune Ltd",
        "exp_date": str(date.today()),
        "init_qty": 500,
        "tot_cost": 800.0
    }
    sample_batch_exp_today2 = {
        "product": created_prods[1].id,
        "supplier": "Jumbo Ltd",
        "exp_date": str(date.today()),
        "init_qty": 499,
        "tot_cost": 799.0
    }
    sample_batch_expired = {
        "product": created_prods[2].id,
        "supplier": "Slow food",
        "exp_date": date.today()-timedelta(days=1),
        "init_qty": 3500,
        "tot_cost": 900.0
    }
    add_many_batches(api_client, 
        (sample_batch_fresh,
        sample_batch_exp_today1, sample_batch_exp_today2,
        sample_batch_expired)
    )

    # get the freshness overview
    url = reverse('inventory:batches_overview')
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    obj = resp.json()
    # check the freshness categories are present
    fresh_batches = obj['fresh']
    today_batches = obj['today']
    expired_batches = obj['expired']
    assert len(fresh_batches) == 1
    assert len(today_batches) == 2
    assert len(expired_batches) == 1
    # check the batches are ordered by exp_date
    for prod, sample in zip(today_batches,
                            sorted((sample_batch_exp_today1, sample_batch_exp_today2),
                            key=lambda p: p['exp_date'])):
        assert prod['exp_date'] == sample['exp_date']
        assert prod['supplier'] == sample['supplier']

@pytest.mark.django_db
def test_batch_get_one(api_client, sample_batch):
    url = reverse('inventory:batches')
    resp = api_client.post(url, sample_batch, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    created_batch = resp.json()

    url = reverse('inventory:batch_detail', args=(created_batch['id'],))
    resp = api_client.get(url, format='json')
    assert resp.status_code == status.HTTP_200_OK
    batch = resp.json()
    del batch['id'], batch['pur_date'], batch['curr_qty']
    assert batch == sample_batch

@pytest.mark.django_db
def test_batch_modify_qty(api_client, sample_batch):
    url = reverse('inventory:batches')
    resp = api_client.post(url, sample_batch, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    created_batch = resp.json()

    new_qty = created_batch['curr_qty']-1
    url = reverse('inventory:batch_detail', args=(created_batch['id'],))
    resp = api_client.patch(url, {"curr_qty": new_qty}, format='json')
    assert resp.status_code == status.HTTP_200_OK
    mod_batch = resp.json()
    assert mod_batch['curr_qty'] == new_qty
    # retrieve it and double check
    resp = api_client.get(url, format='json')
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()['curr_qty'] == new_qty

@pytest.mark.django_db
def test_batch_history(api_client, sample_batch):
    url = reverse('inventory:batches')
    resp = api_client.post(url, sample_batch, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    created_batch = resp.json()
    # decrease the qty
    new_qty = created_batch['curr_qty']-1
    url = reverse('inventory:batch_detail', args=(created_batch['id'],))
    resp = api_client.patch(url, {"curr_qty": new_qty}, format='json')
    assert resp.status_code == status.HTTP_200_OK
    # decrease the qty again
    new_qty -= 1
    url = reverse('inventory:batch_detail', args=(created_batch['id'],))
    resp = api_client.patch(url, {"curr_qty": new_qty}, format='json')
    assert resp.status_code == status.HTTP_200_OK
    # retrieve its history
    url = reverse('inventory:batch_history', args=(created_batch['id'],))
    resp = api_client.get(url, format='json')
    assert resp.status_code == status.HTTP_200_OK
    events = resp.json()['events']
    assert len(events) == 2
    assert all(ev['ev_type'] == 'QTY' for ev in events)
    assert events[0]['ev_info'] == f"From {created_batch['curr_qty']} to {new_qty+1}"
    assert events[1]['ev_info'] == f"From {new_qty+1} to {new_qty}"
