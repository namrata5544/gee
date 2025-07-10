from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    return ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
