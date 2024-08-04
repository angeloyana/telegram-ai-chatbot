import google.generativeai as genai

from chatbot.config import settings

genai.configure(
    api_key=settings.GENAI_API_KEY.get_secret_value(), transport='grpc_asyncio'
)

model = genai.GenerativeModel('gemini-1.5-flash')
