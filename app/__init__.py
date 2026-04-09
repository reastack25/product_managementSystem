from flask import Flask
from app.controllers.inventory_controller import inventory_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(inventory_bp)
    return app