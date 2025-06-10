from app import db
from sqlalchemy.sql import func

class Parcel(db.Model):
    """
    Representa a tabela 'parcel' (pacote/pedido) no banco de dados.
    """
    __tablename__ = 'parcel'
    
    id = db.Column(db.Integer, primary_key=True)
    # A data do pedido será preenchida automaticamente com a data atual.
    date = db.Column(db.Date, nullable=False, default=func.current_date())
    # O status do pedido. Ex: 'Pendente', 'Enviado', 'Entregue'.
    status = db.Column(db.String(30), nullable=False, default='Pendente')
    
    # Chave estrangeira para a tabela 'customer'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    
    # Relacionamento para acessar o objeto Customer diretamente de um Parcel
    customer = db.relationship('Customer', backref=db.backref('parcels', lazy=True))

    def __repr__(self):
        """Representação do objeto para debug."""
        return f'<Parcel id={self.id} status={self.status}>'
