from app import db

class Phone(db.Model):
    """
    Representa a tabela 'phone' no banco de dados.
    """
    __tablename__ = 'phone'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False) # Ex: "Celular", "Residencial"
    number = db.Column(db.String(15), nullable=False)
    ddd = db.Column(db.String(3), nullable=False)
    
    # Define a chave estrangeira que liga o telefone a um cliente
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def __repr__(self):
        """Representação do objeto para debug."""
        return f'<Phone ({self.ddd}) {self.number}>'
