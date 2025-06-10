from flask import request, jsonify, Blueprint
from app import db
from app.models.customer import Customer
from app.models.product import Product
from app.models.cart import Cart
from app.schemas.cart_schema import cart_item_schema, cart_items_schema
from marshmallow import ValidationError

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/<int:customer_id>/cart', methods=['POST'])
def add_to_cart(customer_id):
    """Adiciona um produto ao carrinho de um cliente."""
    Customer.query.get_or_404(customer_id)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Nenhum dado de entrada fornecido'}), 400

    try:
        data = cart_item_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
        
    product_id = data['product_id']
    quantity = data['quantity']
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': f'Produto com id {product_id} não encontrado'}), 404
        
    if product.stock < quantity:
        return jsonify({'error': f'Estoque insuficiente para o produto "{product.name}". Disponível: {product.stock}'}), 400
        
    # Verifica se o produto já está no carrinho para atualizar a quantidade
    cart_item = Cart.query.filter_by(customer_id=customer_id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
        
    db.session.commit()
    result = cart_item_schema.dump(cart_item)
    return jsonify(result), 200

@cart_bp.route('/<int:customer_id>/cart', methods=['GET'])
def get_cart(customer_id):
    """Retorna o carrinho de compras de um cliente."""
    Customer.query.get_or_404(customer_id)
    cart_items = Cart.query.filter_by(customer_id=customer_id).all()
    result = cart_items_schema.dump(cart_items)
    return jsonify(result), 200

@cart_bp.route('/cart/<int:cart_item_id>', methods=['DELETE'])
def remove_from_cart(cart_item_id):
    """Remove um item do carrinho."""
    cart_item = Cart.query.get_or_404(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item removido do carrinho com sucesso'}), 200

@cart_bp.route('/<int:customer_id>/cart/clear', methods=['DELETE'])
def clear_cart(customer_id):
    """Limpa todos os itens do carrinho de um cliente."""
    Customer.query.get_or_404(customer_id)
    Cart.query.filter_by(customer_id=customer_id).delete()
    db.session.commit()
    return jsonify({'message': 'Carrinho limpo com sucesso'}), 200
