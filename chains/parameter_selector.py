from utils.groq_llm import get_llm

def extract_parameters_from_query(query: str):
    prompt = f"""
    Extract the following from the user query: coordinates (latitude, longitude), start_date, end_date out of it
    Assume latitude and longitude if not explicity given. 
    If a particular region like city, country or state is given assume any latitude and longitude yourself and prioritise that over direct latitude longitude given to you.
    Query: "{query}"
    
    Strictly respond in JSON format and NOTHING ELSE, no human text ONLY JSON IN THIS FORMAT:
    {{
      "start_date": "",
      "end_date": "",
      "coordinates": []
    }}
    """
    return get_llm().invoke(prompt).content
