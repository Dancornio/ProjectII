from app import ma
from marshmallow import fields

class PhoneSchema(ma.Schema):
    """
    Define como os objetos Phone serão serializados e desserializados.
    """
    id = fields.Int(dump_only=True)
    type = fields.Str(required=True)
    number = fields.Str(required=True)
    ddd = fields.Str(required=True)
    
    # customer_id é dump_only, pois virá da URL da requisição, não do corpo JSON.
    customer_id = fields.Int(dump_only=True)
    
    class Meta:
        ordered = True

# Instância para um único telefone
phone_schema = PhoneSchema()
# Instância para uma lista de telefones
phones_schema = PhoneSchema(many=True)
