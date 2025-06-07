from app import ma
from app.models.category import Category

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        fields = ('id', 'name')  # Adicione esta linha

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
