from app import db

class Customer(db.Model):
    """
    Representa a tabela 'customer' no banco de dados.
    """
    __tablename__ = 'customer'
    
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Representação do objeto para debug."""
        return f'<Customer {self.name or self.email}>'
