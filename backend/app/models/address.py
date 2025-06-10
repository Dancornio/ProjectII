from app import db

class Address(db.Model):
    """
    Representa a tabela 'adress' no banco de dados.
    """
    __tablename__ = 'adress'
    
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    
    # Define a chave estrangeira que liga o endereço a um cliente
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def __repr__(self):
        """Representação do objeto para debug."""
        return f'<Address {self.street}, {self.city}>'
