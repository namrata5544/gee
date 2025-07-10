from chains.parameter_selector import extract_parameters_from_query
from chains.dataset_selector import select_dataset
from chains.data_fetcher import fetch_data_from_gee
from chains.data_analyzer import analyze_data
from chains.summarizer import summarize_findings

query = "What is the rainfall trend over the past 10 years in Kerala?"

# Step 1: Extract region, date, coords
params = eval(extract_parameters_from_query(query))
print("Params:", params)

# Step 2: Choose dataset(s)
selected = eval(select_dataset(query))
dataset_name = selected["chosen_datasets"][0]
print("Selected dataset:", dataset_name)

# Step 3: Get data from GEE
gee_output = fetch_data_from_gee(params["region"], params["start_date"], params["end_date"], dataset_name)

# Step 4: Analyze data
analysis_result = analyze_data()
print("Analysis:", analysis_result)

# Step 5: Summarize
summary = summarize_findings(analysis_result)
print("Summary:", summary)
