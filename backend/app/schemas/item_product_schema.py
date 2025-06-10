from app import ma
from marshmallow import fields
# Importa o schema de Produto para aninhá-lo na resposta
from app.schemas.product_schema import ProductSchema

class ItemProductSchema(ma.Schema):
    """
    Define como os objetos ItemProduct serão serializados e desserializados.
    """
    id = fields.Int(dump_only=True)
    quantity = fields.Int(required=True)
    
    # O preço e o parcel_id são apenas para saída (dump_only), 
    # pois serão definidos pela lógica do backend, não pela entrada do usuário.
    price = fields.Decimal(as_string=True, places=2, dump_only=True)
    parcel_id = fields.Int(dump_only=True)

    # Para a criação (entrada), esperamos apenas o ID do produto.
    product_id = fields.Int(required=True, load_only=True)

    # Para a exibição (saída), mostramos o objeto completo do produto.
    product = fields.Nested(ProductSchema, dump_only=True)
    
    class Meta:
        ordered = True
        
item_product_schema = ItemProductSchema()
items_product_schema = ItemProductSchema(many=True)