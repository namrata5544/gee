import json
from chains.parameter_selector import extract_parameters_from_query
from chains.dataset_selector import select_dataset
from chains.data_fetcher import fetch_data_from_gee
from chains.data_analyzer import analyze_data
from chains.summarizer import summarize_findings

query = "What is the rainfall trend over the past 10 years in Kerala?"
# extract region, duration
params = json.loads(extract_parameters_from_query(query))
# extract required dataset
selected = json.loads(select_dataset(query))


dataset_name = selected["chosen_datasets"][0]
print("Selected dataset:", dataset_name)

# Step 3: Get data from GEE
gee_output = fetch_data_from_gee(
    region=params.get("region"),
    start_date=params.get("start_date"),
    end_date=params.get("end_date"),
    dataset_name=dataset_name
)

# Step 4: Analyze data
analysis_result = analyze_data(gee_output)
print("Analysis:", analysis_result)

# Step 5: Summarize
summary = summarize_findings(analysis_result)
print("Summary:", summary)
