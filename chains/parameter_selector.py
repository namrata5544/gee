from datetime import date, timedelta
from utils.groq_llm import get_llm

def extract_parameters_from_query(query: str) -> str:
    today = date.today()
    default_end   = today.strftime("%Y-%m-%d")
    default_end = (today - timedelta(days=14)).strftime("%Y-%m-%d")
    default_start = (today - timedelta(days=182)).strftime("%Y-%m-%d")  # 0.5 year ≈ 182 days

    prompt = f"""
You are a JSON‑only function. Parse the user’s text and output **exactly** this object—nothing more:

{{
  "start_date": "",   // YYYY‑MM‑DD
  "end_date": "",     // YYYY‑MM‑DD
  "coordinates": []   // [lat, lon] as floats
}}

Rules:
1. If the query lacks **end_date**, use "{default_end}" (today).
2. If the query lacks **start_date**, set it to six months earlier: "{default_start}".
3. If the query names a place but no lat/lon, invent any plausible pair for that place.
4. Do **not** wrap the JSON in markdown or prose. Produce one valid JSON object and nothing else.

Query: \"\"\"{query}\"\"\"
"""
    return get_llm().invoke(prompt).content  # safe_json_parse will validate
