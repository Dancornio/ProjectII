# app/routes/customer_routes.py

from flask import request, jsonify, Blueprint
from app import db, bcrypt
from app.models.customer import Customer
from app.schemas.customer_schema import customer_schema, customers_output_schema, customer_output_schema
from marshmallow import ValidationError
from validate_docbr import CPF

# Cria um Blueprint para organizar as rotas de cliente
customers_bp = Blueprint('customers_bp', __name__)


@customers_bp.route('/', methods=['POST'])
def create_customer():
    """Cria um novo cliente."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Nenhum dado de entrada fornecido'}), 400

    try:
        # Valida os dados de entrada com o schema
        data = customer_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422 # Unprocessable Entity

     # --- INÍCIO DA VALIDAÇÃO DE CPF ---
    cpf_validator = CPF()
    # Pega o CPF do payload validado pelo schema
    cpf_to_validate = data['cpf']

    if not cpf_validator.validate(cpf_to_validate):
        return jsonify({'error': f'O CPF "{cpf_to_validate}" é inválido'}), 400

    # Verifica se o email ou cpf já existem
    if Customer.query.filter_by(email=data['email']).first():
        return jsonify({'error': f'O email "{data["email"]}" já está em uso'}), 409
    if Customer.query.filter_by(cpf=data['cpf']).first():
        return jsonify({'error': f'O CPF "{data["cpf"]}" já está em uso'}), 409

    # Criptografa a senha antes de salvar
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        cpf=data['cpf'],
        password=hashed_password
    )
    
    db.session.add(new_customer)
    db.session.commit()
    
    # Retorna os dados do cliente usando o schema de saída (sem a senha)
    return customer_output_schema.jsonify(new_customer), 201


@customers_bp.route('/', methods=['GET'])
def get_all_customers():
    """Retorna todos os clientes (sem senhas)."""
    all_customers = Customer.query.all()
    # Usa o schema de saída para garantir que as senhas não sejam retornadas
    result = customers_output_schema.dump(all_customers)
    return jsonify(result), 200


@customers_bp.route('/<int:id>', methods=['GET'])
def get_one_customer(id):
    """Retorna um cliente específico pelo ID (sem senha)."""
    customer = Customer.query.get_or_404(id)
    # Usa o schema de saída
    return customer_output_schema.jsonify(customer), 200


@customers_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    """Atualiza um cliente existente."""
    customer = Customer.query.get_or_404(id)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Nenhum dado de entrada fornecido'}), 400

    # Atualiza os campos se eles forem fornecidos no JSON
    customer.name = json_data.get('name', customer.name)
    customer.email = json_data.get('email', customer.email)
    customer.cpf = json_data.get('cpf', customer.cpf)

    # Se uma nova senha for fornecida, criptografa e atualiza
    if 'password' in json_data and json_data['password']:
        customer.password = bcrypt.generate_password_hash(json_data['password']).decode('utf-8')

    db.session.commit()
    
    # Retorna o cliente atualizado (sem senha)
    return customer_output_schema.jsonify(customer), 200


@customers_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    """Deleta um cliente."""
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    
    return jsonify({'message': f'Cliente "{customer.name}" deletado com sucesso'}), 200

