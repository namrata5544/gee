import json
from utils.groq_llm import get_llm

def select_dataset(query: str):
    with open("data/datasets.json") as f:
        datasets = json.load(f)["options"]

    dataset_str = "\n".join([f"{v['name']}: {v['description']} ({v['cadence']})" for v in datasets.values()])

    prompt = f"""
    Choose the best dataset(s) from the list below to answer the query:
    
    Query: {query}
    
    Datasets:
    {dataset_str}
    
    Respond with a JSON object: {{
      "chosen_datasets": ["dataset_name_1", "dataset_name_2"]
    }}
    """

    return get_llm().invoke(prompt).content
