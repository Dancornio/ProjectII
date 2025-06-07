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
        from app.routes.category_routes import categories_bp
        app.register_blueprint(categories_bp, url_prefix='/api/categories')



    # Registrar manipuladores de erro
    #from app.middleware.error_handler import register_error_handlers
    #register_error_handlers(app)
    
    return app