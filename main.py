import os
import json

from flask import Flask, request, jsonify
from dotenv import load_dotenv

from chains.parameter_selector import extract_parameters_from_query
from chains.dataset_selector import select_dataset
from chains.code_generator import generate_gee_code
from chains.code_executor import execute_gee_code
from utils.groq_llm import ChatGroq

# Load all the variables in your .env into the environment
load_dotenv()

app = Flask(__name__)

# Pull the Groq API key from the env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY in environment")

# Instantiate ChatGroq with the API key
chat_groq = ChatGroq(api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")

def safe_json_parse(label, raw_json_str):
    raw_json_str = raw_json_str.strip()
    if not raw_json_str:
        raise ValueError(f"[{label}] Error: LLM returned empty string.")
    try:
        return json.loads(raw_json_str)
    except json.JSONDecodeError as e:
        print(f"[{label}] Error: Failed to parse JSON.\nRaw Output:\n{raw_json_str}")
        raise e

@app.route('/final', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query parameter'}), 400

        query = data['query']

        # Step 1: Extract parameters from query
        raw_params_output = extract_parameters_from_query(query)
        params = safe_json_parse("extract_parameters_from_query", raw_params_output)

        # Step 2: Select dataset and analysis type
        raw_selected_output = select_dataset(query)
        selected = safe_json_parse("select_dataset", raw_selected_output)

        # Step 3: Generate GEE code
        gee_code = generate_gee_code(
            coordinates=params.get("coordinates"),
            start_date=params.get("start_date"),
            end_date=params.get("end_date"),
            dataset_instructions=selected.get("analysis")
        )

        # Step 4: Execute the generated GEE code
        execution_result = execute_gee_code(gee_code)

        return jsonify({'final': execution_result})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/initial', methods=['POST'])
def analyze_initial():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query parameter'}), 400

        query = data['query']

        # Step 1: Extract parameters
        raw_params_output = extract_parameters_from_query(query)
        params = safe_json_parse("extract_parameters_from_query", raw_params_output)

        # Step 2: Select dataset and analysis type
        raw_selected_output = select_dataset(query)
        selected = safe_json_parse("select_dataset", raw_selected_output)
        analysis_json = selected.get("analysis", {})

        # Summarize that JSON for human readability
        prompt = (
            "Summarize the following JSON in text for human readability and understanding. "
            "The LLM was assigned to generate this JSON and you have to justify the selection "
            "using the reasons given in the JSON itself:\n\n"
            f"{json.dumps(analysis_json, indent=2)}"
        )
        response = chat_groq.invoke(prompt)
        execution_result = response.content

        return jsonify({'initial': execution_result})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
