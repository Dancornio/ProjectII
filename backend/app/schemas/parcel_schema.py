from app import ma
from marshmallow import fields
# Importa os schemas de Cliente e Item de Produto para aninhá-los
from app.schemas.customer_schema import customer_output_schema
from app.schemas.item_product_schema import items_product_schema

class ParcelSchema(ma.Schema):
    """
    Define como os objetos Parcel serão serializados e desserializados.
    """
    id = fields.Int(dump_only=True)
    date = fields.Date(dump_only=True)
    status = fields.Str(dump_only=True) # O status é gerenciado pelo backend
    
    # Para a criação (entrada), esperamos apenas o ID do cliente.
    customer_id = fields.Int(required=True, load_only=True)

    # Para a exibição (saída), mostramos os objetos completos.
    customer = fields.Nested(customer_output_schema, dump_only=True)
    items = fields.Nested(items_product_schema, dump_only=True)
    
    class Meta:
        ordered = True
        
parcel_schema = ParcelSchema()
parcels_schema = ParcelSchema(many=True)
