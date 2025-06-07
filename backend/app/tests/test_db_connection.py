

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import json

import os

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), 'app', '.env'))

app = Flask(__name__)

config_name = os.getenv('FLASK_CONFIG') or 'default'
if config_name == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DATABASE_URL') or 'postgresql://postgres:5RfSfPgu8MNmXK70@db.ashvqjaitdywtfugxgsj.supabase.co:5432/postgres'
elif config_name == 'production':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://postgres:5RfSfPgu8MNmXK70@db.ashvqjaitdywtfugxgsj.supabase.co:5432/postgres'
else: # default ou testing (ajuste conforme necessário para teste)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DATABASE_URL') or 'postgresql://postgres:5RfSfPgu8MNmXK70@db.ashvqjaitdywtfugxgsj.supabase.co:5432/postgres'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def test_connection():
    try:
        with app.app_context():
            
            db.session.execute(db.text('SELECT 1'))
        print("Conexão com o banco de dados bem-sucedida!")
    except OperationalError as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def consulta():
    try:
        with app.app_context():
           
            query_string = text('SELECT * FROM category WHERE id = 3;')
            result = db.session.execute(query_string)
            
            rows = result.fetchall()
            
            if rows:
                print("Resultado da query:")
                for row in rows:
                    
                    print(row) 
            else:
                print("Nenhum resultado encontrado para a query.")

            # Se você espera apenas uma linha (ou a primeira)
            # first_row = result.fetchone()
            # if first_row:
            #     print(f"Primeira linha: {first_row}")
            # else:
            #     print("Nenhuma linha encontrada.")

            # Não se esqueça de fechar a sessão ou fazer commit se fizer alterações (não é o caso aqui para SELECT)
            # db.session.commit() ou db.session.close() se necessário
            
        print("Query executada com sucesso!")

    except ProgrammingError as e:
        print(f"Erro de SQL (verifique se a tabela 'category' existe e a query está correta): {e}")
    except OperationalError as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")



def insert_category(category_nome):
    try:
        with app.app_context():
            
            query_string = text("INSERT INTO category (name) VALUES (:name);")

            result = db.session.execute(query_string, {"name":category_nome})

            db.session.commit()

            print(f"Categoria '{category_nome}' inserida com sucesso mo vei")
    except IntegrityError as e:
        db.session.rollback() # Desfaz a transação em caso de erro (ex: nome duplicado se houver constraint UNIQUE)
        print(f"Erro de integridade ao inserir categoria (ex: nome já existe?): {e}")
        return None
    except ProgrammingError as e:
        db.session.rollback()
        print(f"Erro de SQL (verifique se a tabela 'category' e a coluna 'name' existem): {e}")
        return None
    except OperationalError as e:
        print(f"Erro de conexão com o banco de dados: {e}")
        return None
    except Exception as e:
        db.session.rollback()
        print(f"Ocorreu um erro inesperado ao inserir categoria: {e}")
        return None

def inserir_custumer(password, email, cpf, nome ):
    try:
        with app.app_context():
            query_string = text("INSERT INTO customer (password, email, cpf, name) VALUES (:password, :email, :cpf, :name)")
            db.session.execute(query_string, {"password": password, "email": email, "cpf": cpf, "name": nome})
            db.session.commit()
            print(f"cliente '{nome}' criado com sucesso")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Erro de integridade ao inserir categoria (ex: nome já existe?): {e}")
        return None
    except ProgrammingError as e:
        db.session.rollback()
        print(f"Erro de SQL (verifique se a tabela 'category' e a coluna 'name' existem): {e}")
        return None
    except OperationalError as e:
        print(f"Erro de conexão com o banco de dados: {e}")
        return None
    except Exception as e:
        db.session.rollback()
        print(f"Ocorreu um erro inesperado ao inserir categoria: {e}")
        return None

@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        with app.app_context():
            query_string = text('SELECT * FROM category')
            result = db.session.execute(query_string)
            categories = [dict(row) for row in result.fetchall()]
            return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    get_categories()
    inserir_custumer('senha123', 'vini@mail.com', '09092121', 'Vini')