from utils.groq_llm import get_llm

def extract_parameters_from_query(query: str):
    prompt = f"""
    Extract the following from the user query: coordinates (latitude, longitude), start_date, end_date out of it
    
    Query: "{query}"
    
    Respond in JSON format:
    {{
      "start_date": "",
      "end_date": "",
      "coordinates": []
    }}
    """
    return get_llm().invoke(prompt).content
