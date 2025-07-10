from utils.groq_llm import get_llm

def extract_parameters_from_query(query: str):
    prompt = f"""
    Extract the following from the user query: region name, start_date, end_date, and coordinates if any.
    
    Query: "{query}"
    
    Respond in JSON format:
    {{
      "region": "",
      "start_date": "",
      "end_date": "",
      "coordinates": []
    }}
    """
    return get_llm().invoke(prompt).content
