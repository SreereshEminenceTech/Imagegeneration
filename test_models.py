from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Looking for models supporting generateContent...")
for m in client.models.list():
    if "generateContent" in m.supported_actions and getattr(m, "supported_generation_methods", None) != []:
        print(f"- {m.name}")
        
print("Done")
