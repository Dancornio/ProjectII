from app import db


class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)  # Supondo que a tabela tenha uma coluna 'name'

    def __repr__(self):
        return f'<Category {self.name}>'

