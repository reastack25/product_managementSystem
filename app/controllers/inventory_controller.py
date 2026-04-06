from flask import Blueprint, request, jsonify
from app.models import inventory_model
from app.models.product_model import fetch_product_by_barcode, search_products_by_name

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory', methods=['GET'])
def get_all_items():
    """Fetch all inventory items."""
    items = inventory_model.load_items()
    return jsonify(items), 200

@inventory_bp.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Fetch a single item by ID."""
    item = inventory_model.get_item(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({'error': 'Item not found'}), 404

@inventory_bp.route('/inventory', methods=['POST'])
def add_item():
    """Add a new item. Optionally accepts barcode or name to fetch from external API."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

        barcode = data.get('barcode')
    if barcode:
        product = fetch_product_by_barcode(barcode)
        if product:            
            data.update(product)
        else:
            return jsonify({'error': 'Product not found by barcode'}), 404

    name = data.get('name')
    if not barcode and name:
        products = search_products_by_name(name)
        if products:            
            data.update(products[0])
        else:
            return jsonify({'error': 'No products found with that name'}), 404

 
    if 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

    data.setdefault('quantity', 0)
    data.setdefault('price', 0.0)

    new_item = inventory_model.add_item(data)
    return jsonify(new_item), 201

@inventory_bp.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    """Update an existing item. Only fields provided are updated."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    updated = inventory_model.update_item(item_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Item not found'}), 404

@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item by ID."""
    success = inventory_model.delete_item(item_id)
    if success:
        return '', 204
    return jsonify({'error': 'Item not found'}), 404