from app import ma
from marshmallow import fields
# Importa o schema de Categoria para aninhá-lo aqui
from app.schemas.category_schema import CategorySchema 

class ProductSchema(ma.Schema):
    """
    Define como os objetos Product serão serializados e desserializados.
    """
    id = fields.Int(dump_only=True) # Apenas saída
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Decimal(as_string=True, places=2, required=True)
    stock = fields.Int(required=True)
    image = fields.Str(allow_none=True)
    is_active = fields.Bool(dump_default=True)
    
    # Para a criação (entrada), esperamos apenas o ID da categoria
    category_id = fields.Int(required=True, load_only=True)
    
    # Para a exibição (saída), mostramos o objeto completo da categoria
    category = fields.Nested(CategorySchema, dump_only=True)
    
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    class Meta:
        ordered = True
        
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
