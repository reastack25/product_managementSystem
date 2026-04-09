import pytest
import json
import tempfile
import os
from unittest.mock import patch
from app.models import inventory_model
from app.config import INVENTORY_FILE

@pytest.fixture
def temp_inventory_file():
    """Create a temporary file for testing."""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write('[]')
        temp_path = f.name
    # Patch the INVENTORY_FILE constant to use the temp file
    with patch('app.models.inventory_model.INVENTORY_FILE', temp_path):
        yield temp_path
    os.unlink(temp_path)

def test_load_items_empty(temp_inventory_file):
    items = inventory_model.load_items()
    assert items == []

def test_add_item(temp_inventory_file):
    item = inventory_model.add_item({'name': 'Test', 'quantity': 5, 'price': 10.0})
    assert item['id'] == 1
    items = inventory_model.load_items()
    assert len(items) == 1
    assert items[0]['name'] == 'Test'

def test_update_item(temp_inventory_file):
    inventory_model.add_item({'name': 'Old'})
    updated = inventory_model.update_item(1, {'name': 'New', 'price': 15.0})
    assert updated['name'] == 'New'
    assert updated['price'] == 15.0
    item = inventory_model.get_item(1)
    assert item['name'] == 'New'

def test_delete_item(temp_inventory_file):
    inventory_model.add_item({'name': 'Test'})
    assert inventory_model.delete_item(1) == True
    assert inventory_model.get_item(1) is None
    assert inventory_model.delete_item(99) == False