import json
from utils.groq_llm import get_llm

def select_dataset(query: str):
    # Load dataset options
    with open("data/datasets.json") as f:
        datasets = json.load(f)

    # Load additional natural language instructions
    with open("data/instructions.txt") as f:
        instructions = f.read().strip()

    # Load expected return JSON format (just the analysis key)
    with open("data/dataset_return_format.json") as f:
        analysis = json.load(f)

    # Build prompt
    prompt = f"""
🧠 You are a structured Earth data assistant.

Your job is to generate a **strict JSON response** using the fixed format below by analyzing the user query and selecting appropriate dataset(s), parameters, and analysis types.

---

📝 QUERY:
{query}

---

📦 DATASET OPTIONS:
You may only choose from the following dataset options (name, cadence, parameters):

{json.dumps(datasets, indent=2)}

---

📋 INSTRUCTIONS:
{instructions}

---

🧾 RESPONSE FORMAT:
{json.dumps(analysis, indent=2)}
"""
    return get_llm().invoke(prompt).content
