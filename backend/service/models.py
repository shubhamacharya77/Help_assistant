from langchain_groq import ChatGroq
import os 

class Models():
    def __init__(self):
        pass 

    def chat_model(self):
        return ChatGroq(model="llama-3.1-8b-instant",api_key=os.getenv("GROQ_API_KEY"))

