from dotenv import load_dotenv
import os

load_dotenv()

PICTURE_KEY = os.getenv("PICTURE_KEY")  # ключ для генерации (Kandinsky)
KEY = os.getenv("KEY") # ключ для LLM (DeepSeek)
