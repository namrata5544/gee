import json
from chains.parameter_selector import extract_parameters_from_query
from chains.dataset_selector import select_dataset
from chains.code_generator import generate_gee_code
from chains.code_executor import execute_gee_code

def safe_json_parse(label, raw_json_str):
    raw_json_str = raw_json_str.strip()
    if not raw_json_str:
        raise ValueError(f"[{label}] Error: LLM returned empty string.")
    try:
        return json.loads(raw_json_str)
    except json.JSONDecodeError as e:
        print(f"[{label}] Error: Failed to parse JSON.\nRaw Output:\n{raw_json_str}")
        raise e

query = "Compare rainfall and NDVI over the past 5 years in Kerala?"

# Step 1: Extract parameters from query (coordinates, start_date, end_date)
raw_params_output = extract_parameters_from_query(query)
params = safe_json_parse("extract_parameters_from_query", raw_params_output)

# Step 2: Select dataset and analysis type
raw_selected_output = select_dataset(query)
selected = safe_json_parse("select_dataset", raw_selected_output)

print("Extracted parameters:", params)
print("Selected analysis:", selected)

# Step 3: Generate GEE code
gee_code = generate_gee_code(
    coordinates=params.get("coordinates"),
    start_date=params.get("start_date"),
    end_date=params.get("end_date"),
    dataset_instructions=selected.get("analysis")
)

print("\nGenerated GEE Code:")
print(gee_code)

# Step 4: Execute the generated GEE code
execution_result = execute_gee_code(gee_code)
print(execution_result)
