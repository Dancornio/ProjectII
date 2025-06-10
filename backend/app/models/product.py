from app import db
from sqlalchemy.sql import func

class Product(db.Model):
    """
    Representa a tabela 'product' no banco de dados.
    """
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    # Usando Numeric para representar dinheiro, que é uma prática recomendada.
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Chave estrangeira para a tabela 'category'
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # Timestamps que são gerenciados automaticamente pelo banco de dados
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamento para acessar o objeto Category diretamente de um Produto
    category = db.relationship('Category', backref=db.backref('products', lazy=True))

    def __repr__(self):
        """Representação do objeto para debug."""
        return f'<Product {self.name}>'
