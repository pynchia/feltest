
import pytest
from django.core.exceptions import ValidationError

from inventory.models import Product


# Testing the models can be useful to ensure the models are aligned
# to what we expect them to be and no fortuitous changes
# to them compromise the system.
# If models change, then tests need to change accordingly
# and represent an opportunity to validate such changes


@pytest.mark.django_db
def test_product_create():
    Product.objects.create(name='testprod', weight=1.0)
    assert Product.objects.count() == 1

@pytest.mark.django_db
def test_product_create_invalid_name():
    with pytest.raises(ValidationError):
        prod = Product.objects.create(name='')
        prod.full_clean()

@pytest.mark.django_db
def test_product_create_invalid_weight():
    with pytest.raises(ValueError):
        Product.objects.create(name='testprod', weight='xyz')

# more tests for the other models..., same soup
