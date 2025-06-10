from app import db

class Cart(db.Model):
    """
    Representa a tabela 'cart' (carrinho de compras) no banco de dados.
    """
    __tablename__ = 'cart'
    
    # O DDL usa 'cart_id', mas a convenção do SQLAlchemy é usar 'id'.
    # Usaremos 'id' na classe e 'cart_id' no banco de dados com `primary_key=True`.
    id = db.Column("cart_id", db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Chaves estrangeiras
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    # Relacionamentos para fácil acesso aos objetos
    customer = db.relationship('Customer', backref=db.backref('cart_items', lazy=True, cascade="all, delete-orphan"))
    product = db.relationship('Product')

    def __repr__(self):
        """Representação do objeto para debug."""
        return f'<CartItem customer_id={self.customer_id} product_id={self.product_id} quantity={self.quantity}>'
