import os
from dotenv import load_dotenv
load_dotenv()

print(os.environ.get('DATABASE_URL'))
print(os.environ.get('SECRET_KEY'))

print("ola")
