from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    return ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")
