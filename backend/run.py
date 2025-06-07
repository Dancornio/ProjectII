#import os

# --- INÍCIO DA CORREÇÃO ---
# Adiciona o diretório raiz do projeto (a pasta 'backend') ao PYTHONPATH.
# Isso garante que as importações como 'from app.models...' funcionem corretamente.
#sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

# Cria a aplicação usando a fábrica
app = create_app()

if __name__ == '__main__':
    # Para produção, use um servidor WSGI como Gunicorn
    app.run(debug=True, port=5000)
