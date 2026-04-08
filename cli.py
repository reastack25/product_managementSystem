import click
import requests

API_BASE = 'http://localhost:5000'

@click.group()
def cli():
    """Inventory Management CLI"""
    pass

@cli.command()
def list():
    """List all inventory items."""
    try:
        resp = requests.get(f'{API_BASE}/inventory')
        resp.raise_for_status()
        items = resp.json()
        if not items:
            click.echo('No items found.')
        for item in items:
            click.echo(f"{item['id']}: {item['name']} - Qty: {item['quantity']} - Price: ${item['price']}")
    except requests.RequestException as e:
        click.echo(f'Error: {e}', err=True)

@cli.command()
@click.argument('item_id', type=int)
def get(item_id):
    """Get a single item by ID."""
    try:
        resp = requests.get(f'{API_BASE}/inventory/{item_id}')
        if resp.status_code == 404:
            click.echo('Item not found.')
        else:
            resp.raise_for_status()
            item = resp.json()
            click.echo(f"ID: {item['id']}\nName: {item['name']}\nBrand: {item.get('brand', 'N/A')}\nQuantity: {item['quantity']}\nPrice: ${item['price']}")
    except requests.RequestException as e:
        click.echo(f'Error: {e}', err=True)

@cli.command()
@click.option('--name', prompt='Name', help='Product name')
@click.option('--quantity', default=0, type=int, help='Quantity')
@click.option('--price', default=0.0, type=float, help='Price')
@click.option('--barcode', help='Product barcode to fetch details')
def add(name, quantity, price, barcode):
    """Add a new inventory item."""
    data = {
        'name': name,
        'quantity': quantity,
        'price': price
    }
    if barcode:
        data['barcode'] = barcode

    try:
        resp = requests.post(f'{API_BASE}/inventory', json=data)
        if resp.status_code == 201:
            item = resp.json()
            click.echo(f"Added item ID: {item['id']}")
        else:
            click.echo(f"Error: {resp.json().get('error', 'Unknown error')}")
    except requests.RequestException as e:
        click.echo(f'Error: {e}', err=True)

@cli.command()
@click.argument('item_id', type=int)
@click.option('--name', help='New name')
@click.option('--quantity', type=int, help='New quantity')
@click.option('--price', type=float, help='New price')
def update(item_id, name, quantity, price):
    """Update an inventory item."""
    data = {}
    if name:
        data['name'] = name
    if quantity is not None:
        data['quantity'] = quantity
    if price is not None:
        data['price'] = price

    if not data:
        click.echo('No update fields provided.')
        return

    try:
        resp = requests.patch(f'{API_BASE}/inventory/{item_id}', json=data)
        if resp.status_code == 200:
            click.echo('Item updated.')
        elif resp.status_code == 404:
            click.echo('Item not found.')
        else:
            click.echo(f'Error: {resp.json().get("error", "Unknown error")}')
    except requests.RequestException as e:
        click.echo(f'Error: {e}', err=True)

@cli.command()
@click.argument('item_id', type=int)
def delete(item_id):
    """Delete an inventory item."""
    try:
        resp = requests.delete(f'{API_BASE}/inventory/{item_id}')
        if resp.status_code == 204:
            click.echo('Item deleted.')
        elif resp.status_code == 404:
            click.echo('Item not found.')
        else:
            click.echo(f'Error: {resp.json().get("error", "Unknown error")}')
    except requests.RequestException as e:
        click.echo(f'Error: {e}', err=True)

@cli.command()
@click.option('--barcode', help='Search by barcode')
@click.option('--name', help='Search by name')
def fetch(barcode, name):
    """Fetch product details from external API (does not add to inventory)."""
    from app.models.product_model import fetch_product_by_barcode, search_products_by_name

    if barcode:
        product = fetch_product_by_barcode(barcode)
        if product:
            click.echo(f"Name: {product['name']}\nBrand: {product['brand']}\nIngredients: {product['ingredients']}")
        else:
            click.echo('Product not found.')
    elif name:
        products = search_products_by_name(name)
        if products:
            for p in products:
                click.echo(f"Name: {p['name']} | Brand: {p['brand']} | Barcode: {p['barcode']}")
        else:
            click.echo('No products found.')
    else:
        click.echo('Please provide --barcode or --name.')

if __name__ == '__main__':
    cli()