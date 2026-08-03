import os 
from google import genai
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")
API_AGENT = os.getenv("API_KEY_AGENT")


# client = genai.Client()

# def analyzing_with_model():
    
#     model = client.models.generate_content(
#         model="gemini-2.6-flash", 
#         contents="Her skal innholdet være som skal spørre.")


#     return model