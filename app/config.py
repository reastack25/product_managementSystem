import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')
INVENTORY_FILE = os.path.join(DATA_DIR, 'inventory.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

OPENFOODFACTS_API_URL = "https://world.openfoodfacts.org/api/v0/product/{}.json"