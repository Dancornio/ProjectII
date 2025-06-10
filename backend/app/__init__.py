from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from app.config import config

# Inicialização das extensões
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
bcrypt = Bcrypt()
ma = Marshmallow()

def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    

    with app.app_context():
        # --- REGISTRO DOS BLUEPRINTS (ROTAS) ---
        from app.routes.customer_routes import customers_bp
        app.register_blueprint(customers_bp, url_prefix='/api/customers')

        from app.routes.category_routes import categories_bp
        app.register_blueprint(categories_bp, url_prefix='/api/categories')

        from app.routes.address_routes import addresses_bp
        app.register_blueprint(addresses_bp, url_prefix='/api/customers')

        from app.routes.phone_routes import phones_bp
        app.register_blueprint(phones_bp, url_prefix='/api/customers')

        from app.routes.product_routes import products_bp
        app.register_blueprint(products_bp, url_prefix='/api/products')

        from app.routes.parcel_routes import parcels_bp
        app.register_blueprint(parcels_bp, url_prefix='/api/parcels')

        from app.routes.item_product_routes import item_products_bp
        app.register_blueprint(item_products_bp, url_prefix='/api/parcels')

        from app.routes.cart_routes import cart_bp
        app.register_blueprint(cart_bp, url_prefix='/api/customers')
    # Registrar manipuladores de erro
    #from app.middleware.error_handler import register_error_handlers
    #register_error_handlers(app)
    
    return app