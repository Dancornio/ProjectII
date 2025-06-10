from app import ma
from marshmallow import fields
from app.schemas.product_schema import ProductSchema

class CartSchema(ma.Schema):
    """
    Define como os objetos Cart (itens do carrinho) serão serializados.
    """
    id = fields.Int(dump_only=True)
    quantity = fields.Int(required=True)
    
    # Para a criação (entrada), esperamos apenas o ID do produto e a quantidade.
    product_id = fields.Int(required=True, load_only=True)
    customer_id = fields.Int(dump_only=True)
    
    # Para a exibição (saída), mostramos o objeto completo do produto.
    product = fields.Nested(ProductSchema, dump_only=True)
    
    class Meta:
        ordered = True

cart_item_schema = CartSchema()
cart_items_schema = CartSchema(many=True)