from app import db

class ItemProduct(db.Model):
    """
    Representa a tabela 'itemproduct' (item de um pedido) no banco de dados.
    """
    __tablename__ = 'itemproduct'
    
    id = db.Column(db.Integer, primary_key=True)
    # Usando Numeric para representar o preço no momento da compra.
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Chaves estrangeiras
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcel.id'), nullable=False)
    
    # Relacionamentos para fácil acesso aos objetos
    # O backref em 'parcel' permite acessar os itens a partir de um objeto Parcel (ex: meu_pacote.items)
    product = db.relationship('Product')
    parcel = db.relationship('Parcel', backref=db.backref('items', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        """Representação do objeto para debug."""
        return f'<ItemProduct id={self.id} product_id={self.product_id} quantity={self.quantity}>'
