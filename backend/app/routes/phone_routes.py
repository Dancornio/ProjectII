from flask import request, jsonify, Blueprint
from app import db
from app.models.customer import Customer
from app.models.phone import Phone
from app.schemas.phone_schema import phone_schema, phones_schema
from marshmallow import ValidationError

phones_bp = Blueprint('phones_bp', __name__)

@phones_bp.route('/<int:customer_id>/phones', methods=['POST'])
def add_phone_to_customer(customer_id):
    """Adiciona um novo telefone para um cliente específico."""
    Customer.query.get_or_404(customer_id)
    
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Nenhum dado de entrada fornecido'}), 400

    try:
        data = phone_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    new_phone = Phone(
        type=data['type'],
        number=data['number'],
        ddd=data['ddd'],
        customer_id=customer_id
    )

    db.session.add(new_phone)
    db.session.commit()

    return phone_schema.jsonify(new_phone), 201

@phones_bp.route('/<int:customer_id>/phones', methods=['GET'])
def get_customer_phones(customer_id):
    """Retorna todos os telefones de um cliente específico."""
    Customer.query.get_or_404(customer_id)
    
    phones = Phone.query.filter_by(customer_id=customer_id).all()
    return phones_schema.jsonify(phones), 200

@phones_bp.route('/phones/<int:phone_id>', methods=['PUT'])
def update_phone(phone_id):
    """Atualiza um telefone específico."""
    phone = Phone.query.get_or_404(phone_id)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Nenhum dado de entrada fornecido'}), 400
        
    try:
        data = phone_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422

    for key, value in data.items():
        setattr(phone, key, value)

    db.session.commit()
    return phone_schema.jsonify(phone), 200

@phones_bp.route('/phones/<int:phone_id>', methods=['DELETE'])
def delete_phone(phone_id):
    """Deleta um telefone específico."""
    phone = Phone.query.get_or_404(phone_id)
    db.session.delete(phone)
    db.session.commit()

    return jsonify({'message': 'Telefone deletado com sucesso'}), 200
