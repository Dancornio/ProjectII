# app/schemas/customer_schema.py

from app import ma
from marshmallow import fields, validate

class CustomerSchema(ma.Schema):
    """
    Define como os objetos Customer serão serializados e desserializados.
    """
    # --- CORREÇÃO: Todos os campos agora são declarados explicitamente ---

    # dump_only significa que este campo só aparecerá em respostas da API (output),
    # mas não será esperado em requisições de criação (input).
    id = fields.Int(dump_only=True)
    
    # load_only significa que este campo só será aceito em requisições (input),
    # mas nunca aparecerá nas respostas da API (output) por segurança.
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))
    
    # required=True significa que estes campos são obrigatórios para criar um cliente.
    email = fields.Email(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    cpf = fields.Str(required=True, validate=validate.Length(equal=11))
    
    class Meta:
        # A linha 'fields' foi removida porque os campos já estão definidos acima.
        ordered = True

# Instância para validar a entrada de dados (requisições POST/PUT)
customer_schema = CustomerSchema()

# Instância para formatar a saída de dados (respostas GET), excluindo a senha
# Mesmo com 'load_only', é uma boa prática ser explícito.
customer_output_schema = CustomerSchema(exclude=('password',))
customers_output_schema = CustomerSchema(many=True, exclude=('password',))
