import os
import tinker
from tinker import ServiceClient
from dotenv import load_dotenv

load_dotenv("backend/.env")
API_KEY = os.getenv("TINKER_API_KEY")
os.environ["TINKER_API_KEY"] = API_KEY

client = ServiceClient()
caps = client.get_server_capabilities()
print("Supported Models:")
for model in caps.supported_models:
    print(f"- {model}")
