from flask import request, jsonify, Blueprint
from app import db
from app.models.category import Category
from app.schemas.category_schema import category_schema, categories_schema

# Cria um Blueprint para organizar as rotas de categoria
categories_bp = Blueprint('categories_bp', __name__)


@categories_bp.route('/', methods=['POST'])
def create_category():
    """Cria uma nova categoria."""
    name = request.json.get('name')
    if not name:
        return jsonify({'error': 'O campo "name" é obrigatório'}), 400

    if Category.query.filter_by(name=name).first():
        return jsonify({'error': f'A categoria "{name}" já existe'}), 409 # Conflict

    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    
    return category_schema.jsonify(new_category), 201 # Created

@categories_bp.route('/', methods=['GET'])
def get_all_categories():
    """Retorna todas as categorias."""
    all_categories = Category.query.order_by(Category.name).all()
    result = categories_schema.dump(all_categories)
    return jsonify(result), 200

@categories_bp.route('/<int:id>', methods=['GET'])
def get_one_category(id):
    """Retorna uma categoria específica pelo ID."""
    category = Category.query.get_or_404(id)
    return category_schema.jsonify(category), 200

@categories_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    """Atualiza uma categoria existente."""
    category = Category.query.get_or_404(id)
    
    name = request.json.get('name')
    if not name:
        return jsonify({'error': 'O campo "name" é obrigatório'}), 400

    # Verifica se o novo nome já está em uso por outra categoria
    existing_category = Category.query.filter(Category.name == name, Category.id != id).first()
    if existing_category:
        return jsonify({'error': f'O nome "{name}" já está em uso'}), 409

    category.name = name
    db.session.commit()
    
    return category_schema.jsonify(category), 200

@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    """Deleta uma categoria."""
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'message': f'Categoria "{category.name}" deletada com sucesso'}), 200
