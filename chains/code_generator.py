from utils.groq_llm import get_llm

def generate_gee_code(region, start_date, end_date, dataset):
    prompt = f"""
    Write Google Earth Engine Python API code to fetch {dataset} data for the region "{region}" 
    from "{start_date}" to "{end_date}". Print the extracted values.

    Output should be valid Python code using geemap or ee library. Keep it simple and modular.
    """
    return get_llm().invoke(prompt).content
