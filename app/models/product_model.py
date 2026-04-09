import requests
from app.config import OPENFOODFACTS_API_URL

def fetch_product_by_barcode(barcode):
    """Fetch product details by barcode using OpenFoodFacts API."""
    url = OPENFOODFACTS_API_URL.format(barcode)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 1:  # product found
            product = data['product']
            return {
                'name': product.get('product_name', 'Unknown'),
                'brand': product.get('brands', 'Unknown'),
                'ingredients': product.get('ingredients_text', ''),
                
            }
        else:
            return None
    except requests.RequestException:
        return None

def search_products_by_name(name):
    """Search for products by name (simple search)."""   
    search_url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        'search_terms': name,
        'search_simple': 1,
        'action': 'process',
        'json': 1,
        'page_size': 5  
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        products = []
        for product in data.get('products', []):
            products.append({
                'name': product.get('product_name', 'Unknown'),
                'brand': product.get('brands', 'Unknown'),
                'ingredients': product.get('ingredients_text', ''),
                'barcode': product.get('code', '')
            })
        return products
    except requests.RequestException:
        return []