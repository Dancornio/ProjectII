from flask import request, jsonify, Blueprint
from app import db
from app.models.customer import Customer
from app.models.parcel import Parcel
from app.schemas.parcel_schema import parcel_schema, parcels_schema
from marshmallow import ValidationError

parcels_bp = Blueprint('parcels_bp', __name__)

@parcels_bp.route('/', methods=['POST'])
def create_parcel():
    """Cria um novo pedido (parcel) para um cliente."""
    json_data = request.get_json()
    if not json_data or 'customer_id' not in json_data:
        return jsonify({'error': 'O campo "customer_id" é obrigatório'}), 400
    
    customer_id = json_data['customer_id']
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': f'Cliente com id {customer_id} não encontrado'}), 404
        
    # Cria um novo pedido (parcel) associado ao cliente
    new_parcel = Parcel(customer_id=customer.id)
    
    db.session.add(new_parcel)
    db.session.commit()
    
    result = parcel_schema.dump(new_parcel)
    return jsonify(result), 201

@parcels_bp.route('/', methods=['GET'])
def get_all_parcels():
    """Retorna todos os pedidos."""
    parcels = Parcel.query.order_by(Parcel.date.desc()).all()
    result = parcels_schema.dump(parcels)
    return jsonify(result), 200

@parcels_bp.route('/<int:id>', methods=['GET'])
def get_one_parcel(id):
    """Retorna um pedido específico, com cliente e itens."""
    parcel = Parcel.query.get_or_404(id)
    result = parcel_schema.dump(parcel)
    return jsonify(result), 200

@parcels_bp.route('/<int:id>', methods=['PUT'])
def update_parcel_status(id):
    """Atualiza o status de um pedido."""
    parcel = Parcel.query.get_or_404(id)
    json_data = request.get_json()
    if not json_data or 'status' not in json_data:
        return jsonify({'error': 'O campo "status" é obrigatório'}), 400
        
    parcel.status = json_data['status']
    db.session.commit()
    
    result = parcel_schema.dump(parcel)
    return jsonify(result), 200

@parcels_bp.route('/<int:id>', methods=['DELETE'])
def delete_parcel(id):
    """Deleta um pedido e seus itens associados."""
    # A configuração 'cascade' no modelo ItemProduct garante que os itens
    # também serão deletados do banco de dados.
    parcel = Parcel.query.get_or_404(id)
    db.session.delete(parcel)
    db.session.commit()
    
    return jsonify({'message': f'Pedido com id {id} deletado com sucesso'}), 200