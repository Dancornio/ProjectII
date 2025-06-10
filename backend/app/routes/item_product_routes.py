from flask import request, jsonify, Blueprint
from app import db
from app.models.product import Product
from app.models.parcel import Parcel # IMPORTANTE: Requer que o modelo Parcel exista
from app.models.item_product import ItemProduct
from app.schemas.item_product_schema import item_product_schema, items_product_schema
from marshmallow import ValidationError

item_products_bp = Blueprint('item_products_bp', __name__)

@item_products_bp.route('/<int:parcel_id>/items', methods=['POST'])
def add_item_to_parcel(parcel_id):
    """Adiciona um novo item (produto) a um pacote (parcel)."""
    # Garante que o pacote (parcel) existe. Requer que o modelo Parcel seja criado.
    Parcel.query.get_or_404(parcel_id)
    
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Nenhum dado de entrada fornecido'}), 400

    try:
        data = item_product_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
        
    product_id = data['product_id']
    quantity = data['quantity']
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': f'Produto com id {product_id} não encontrado'}), 404
        
    if product.stock < quantity:
        return jsonify({'error': f'Estoque insuficiente para o produto "{product.name}". Disponível: {product.stock}'}), 400

    # Cria o novo item
    new_item = ItemProduct(
        price=product.price, # Pega o preço atual do produto
        quantity=quantity,
        product_id=product_id,
        parcel_id=parcel_id
    )
    
    # Reduz o estoque do produto
    product.stock -= quantity

    db.session.add(new_item)
    db.session.commit()

    result = item_product_schema.dump(new_item)
    return jsonify(result), 201

@item_products_bp.route('/<int:parcel_id>/items', methods=['GET'])
def get_parcel_items(parcel_id):
    """Retorna todos os itens de um pacote específico."""
    Parcel.query.get_or_404(parcel_id)
    items = ItemProduct.query.filter_by(parcel_id=parcel_id).all()
    result = items_product_schema.dump(items)
    return jsonify(result), 200

@item_products_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Deleta um item e devolve a quantidade ao estoque."""
    item = ItemProduct.query.get_or_404(item_id)
    
    # Devolve a quantidade ao estoque do produto
    product = Product.query.get(item.product_id)
    if product:
        product.stock += item.quantity
        
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Item deletado com sucesso e estoque atualizado'}), 200