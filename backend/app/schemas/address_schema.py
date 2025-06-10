from app import ma
from marshmallow import fields

class AddressSchema(ma.Schema):
    """
    Define como os objetos Address serão serializados e desserializados.
    """
    id = fields.Int(dump_only=True)
    state = fields.Str(required=True)
    city = fields.Str(required=True)
    district = fields.Str(required=True)
    street = fields.Str(required=True)
    cep = fields.Str(required=True)
    
    # O customer_id é dump_only para ser incluído na resposta, 
    # mas não será passado no corpo da requisição, pois virá da URL.
    customer_id = fields.Int(dump_only=True)
    
    class Meta:
        ordered = True

# Instância para um único endereço
address_schema = AddressSchema()
# Instância para uma lista de endereços
addresses_schema = AddressSchema(many=True)
