from django.urls import reverse
from rest_framework import status


def add_many_products(api_client, products):
    url = reverse('inventory:products')
    for prod in products:
        resp = api_client.post(url, prod, format='json')
        assert resp.status_code == status.HTTP_201_CREATED
        ret_prod = resp.json()
        assert ret_prod['name'] == prod['name']

def add_many_batches(api_client, batches):
    url = reverse('inventory:batches')
    for batch in batches:
        resp = api_client.post(url, batch, format='json')
        assert resp.status_code == status.HTTP_201_CREATED
        ret_batch = resp.json()
        assert ret_batch['supplier'] == batch['supplier']
