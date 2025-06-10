from flask import request, jsonify, Blueprint
from app import db
from app.models.customer import Customer
from app.models.address import Address
from app.schemas.address_schema import address_schema, addresses_schema
from marshmallow import ValidationError

# Usamos um Blueprint para aninhar endereços sob clientes
# O prefixo da URL será definido ao registrar o Blueprint
addresses_bp = Blueprint('addresses_bp', __name__)

@addresses_bp.route('/<int:customer_id>/addresses', methods=['POST'])
def add_address_to_customer(customer_id):
    """Adiciona um novo endereço para um cliente específico."""
    # Garante que o cliente existe
    Customer.query.get_or_404(customer_id)
    
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Nenhum dado de entrada fornecido'}), 400

    try:
        data = address_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    new_address = Address(
        state=data['state'],
        city=data['city'],
        district=data['district'],
        street=data['street'],
        cep=data['cep'],
        customer_id=customer_id  # Associa o endereço ao cliente da URL
    )

    db.session.add(new_address)
    db.session.commit()

    return address_schema.jsonify(new_address), 201

@addresses_bp.route('/<int:customer_id>/addresses', methods=['GET'])
def get_customer_addresses(customer_id):
    """Retorna todos os endereços de um cliente específico."""
    # Garante que o cliente existe
    Customer.query.get_or_404(customer_id)
    
    addresses = Address.query.filter_by(customer_id=customer_id).all()
    return addresses_schema.jsonify(addresses), 200

@addresses_bp.route('/addresses/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    """Atualiza um endereço específico."""
    address = Address.query.get_or_404(address_id)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Nenhum dado de entrada fornecido'}), 400
        
    try:
        data = address_schema.load(json_data, partial=True) # partial=True permite atualização parcial
    except ValidationError as err:
        return jsonify(err.messages), 422

    for key, value in data.items():
        setattr(address, key, value)

    db.session.commit()
    return address_schema.jsonify(address), 200


@addresses_bp.route('/addresses/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    """Deleta um endereço específico."""
    address = Address.query.get_or_404(address_id)
    db.session.delete(address)
    db.session.commit()

    return jsonify({'message': 'Endereço deletado com sucesso'}), 200
