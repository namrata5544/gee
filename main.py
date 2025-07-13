import json
from chains.parameter_selector import extract_parameters_from_query
from chains.dataset_selector import select_dataset
from chains.code_generator import generate_gee_code
from chains.code_executor import execute_gee_code

query = "What is the rainfall trend over the past 10 years in Kerala?"
# extract coordinates, start_date, end_date
params = json.loads(extract_parameters_from_query(query))
# extract required dataset and analysis parameters
selected = json.loads(select_dataset(query))

print("Extracted parameters:", params)
print("Selected analysis:", selected)


# Generate single GEE code that handles all datasets
gee_code = generate_gee_code(
    coordinates=params.get("coordinates"),
    start_date=params.get("start_date"),
    end_date=params.get("end_date"),
    dataset_instructions=selected.get("analysis")
)

print("\nGenerated GEE Code:")
print(gee_code)

# Step 4: Execute the generated GEE code in sandbox
execution_result = execute_gee_code(gee_code)
