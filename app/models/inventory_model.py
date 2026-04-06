import json
from app.config import INVENTORY_FILE

def load_items():
    try:
        with open(INVENTORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] 

def save_items(items):
    """Save inventory items to the JSON file."""
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(items, f, indent=2)

def get_item(item_id):
    """Retrieve a single item by ID."""
    items = load_items()
    for item in items:
        if item['id'] == item_id:
            return item
    return None

def add_item(item_data):
    """Add a new item, generating a new ID."""
    items = load_items()
    new_id = max([item['id'] for item in items], default=0) + 1
    item_data['id'] = new_id
    items.append(item_data)
    save_items(items)
    return item_data

def update_item(item_id, updated_data):
    items = load_items()
    for i, item in enumerate(items):
        if item['id'] == item_id:
            item.update(updated_data)
            item['id'] = item_id 
            save_items(items)
            return item
    return None

def delete_item(item_id):
    items = load_items()
    new_items = [item for item in items if item['id'] != item_id]
    if len(new_items) == len(items):
        return False  
    save_items(new_items)
    return True