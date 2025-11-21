from dotenv import load_dotenv
import os

print("Tentando carregar .env...")

load_dotenv()

valor = os.getenv("OPENAI_API_KEY")
print("Valor carregado:", valor)
