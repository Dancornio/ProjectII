from flask import request, jsonify, Blueprint
from app import db
from app.models.product import Product
from app.models.category import Category
from app.schemas.product_schema import product_schema, products_schema
from marshmallow import ValidationError

products_bp = Blueprint('products_bp', __name__)

@products_bp.route('/', methods=['POST'])
def create_product():
    """Cria um novo produto."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Nenhum dado de entrada fornecido'}), 400

    try:
        data = product_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    # Garante que a categoria fornecida existe
    category_id = data['category_id']
    if not Category.query.get(category_id):
        return jsonify({'error': f'Categoria com id {category_id} não encontrada'}), 404

    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock'],
        image=data.get('image'),
        is_active=data.get('is_active', True),
        category_id=category_id
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    result = product_schema.dump(new_product)
    return jsonify(result), 201

@products_bp.route('/', methods=['GET'])
def get_all_products():
    """Retorna todos os produtos."""
    products = Product.query.order_by(Product.name).all()
    result = products_schema.dump(products)
    return jsonify(result), 200

@products_bp.route('/<int:id>', methods=['GET'])
def get_one_product(id):
    """Retorna um produto específico pelo ID."""
    product = Product.query.get_or_404(id)
    result = product_schema.dump(product)
    return jsonify(result), 200

@products_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    """Atualiza um produto existente."""
    product = Product.query.get_or_404(id)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Nenhum dado de entrada fornecido'}), 400
        
    try:
        data = product_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422

    # Valida a categoria se ela for alterada
    if 'category_id' in data and not Category.query.get(data['category_id']):
        return jsonify({'error': f'Categoria com id {data["category_id"]} não encontrada'}), 404

    for key, value in data.items():
        setattr(product, key, value)

    db.session.commit()
    result = product_schema.dump(product)
    return jsonify(result), 200

@products_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    """Deleta um produto."""
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': f'Produto "{product.name}" deletado com sucesso'}), 200