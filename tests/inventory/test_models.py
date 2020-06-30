import pytest

from inventory.models import Product


# Testing the models is useful to ensure the models are aligned
# to what we expect them to be and no fortuitous changes
# to them compromise the system.
# Is models change, then tests need to change accordingly
# and represent an opportunity to ponder on such changes

@pytest.mark.django_db
def test_product_create():
    Product.objects.create(name='testprod', weight=1.0)
    assert Product.objects.count() == 1

@pytest.mark.django_db
@pytest.mark.xfail
def test_product_create_invalid_name():
    prod = Product.objects.create(name='')
    prod.full_clean()

@pytest.mark.django_db
@pytest.mark.xfail
def test_product_create_invalid_weight():
    Product.objects.create(name='testprod', weight='xyz')

# more tests for the other models....
