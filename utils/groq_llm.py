from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    return ChatGroq(temperature=0, model_name="llama3-70b-8192")
