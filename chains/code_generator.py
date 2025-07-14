from utils.groq_llm import get_llm
from dotenv import load_dotenv
import os
load_dotenv()
def generate_gee_code(coordinates, start_date, end_date, dataset_instructions):
    lat, lon = coordinates[0], coordinates[1]
    groqq = os.getenv("GROQQ")
    emaill = os.getenv("EMAILL")
    service_dict = os.getenv("SERVICE_DICT")
    
    prompt = f"""
You are an expert in Google Earth Engine (GEE) and statistical analysis.
ONLY RETURN THE PYTHON SCRIPT AND NO UNNECESSARY TEXT SURROUNDING IT AS I HAVE TO DIRECTLY EXECUTE THE CODE IN ENVIRONMENT LATER ON. 
ENSURE THAT THE WHOLE SCRIPT IS SYNTACTICALLY ACCURATE AS I HAVE TO PASS IT IN AN ENVIRONMENT.
You must write a complete Python script that:
1. Uses the GEE Python API to extract parameter data for a given coordinate and time range
2. Dynamically splits the time range into smaller windows (e.g., months, weeks) for better temporal resolution
3. Parallelizes GEE `.getInfo()` calls for each time window
4. Analyzes the resulting time series using Python libraries
5. Summarizes the statistical insights via a Groq LLM

---


📍 REGION: Latitude = {lat}, Longitude = {lon}  
📅 TIME RANGE: {start_date} to {end_date}  
📊 DATASETS & PARAMETERS:  
{dataset_instructions}

---
only use from langchain_groq import ChatGroq
DO NOT USE from langchain.chat_models import ChatGroq
🔹 STEP 1: Required Imports & Initialization

Begin with, this step is crucial and strict do not mess up this or generate anything random here:

```python
import ee
import json
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os
import tempfile
from langchain.chat_models import ChatGroq

SERVICE_ACCOUNT_EMAIL = "{emaill}"

SERVICE_ACCOUNT_DICT = {service_dict}


with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_key_file:
    json.dump(SERVICE_ACCOUNT_DICT, temp_key_file)
    temp_key_file_path = temp_key_file.name

# Authenticate
credentials = ee.ServiceAccountCredentials(SERVICE_ACCOUNT_EMAIL, temp_key_file_path)
ee.Initialize(credentials)

```

🔹 STEP 2: Split Time into Blocks Based on Range

Based on how long the time range {start_date} to {end_date} is divide the time duration into appropriate time blocks such that it generates 
sufficient amount of data to make analysis.

Generate a list of (start, end) tuples representing these time blocks. For example:
⚠️ IMPORTANT: When appending multiple values to a list, always use a tuple. For example:
✅ list.append((a, b)) and not list.append(a, b).

✅ This ensures multiple .getInfo() samples for time series analysis
✅ This logic must be done dynamically based on the actual input range

🔹 STEP 3: For Each Dataset and Parameter, Fetch Multiple Data Points

Loop through input_json["analysis"] dynamically:

```json
{{
  "dataset": "Dataset_ID",
  "parameters": [
    {{ "name": "parameter_name", ... }}
  ]
}}
```

For each (dataset, parameter), do the following:

For each (start, end) time block:
Use ThreadPoolExecutor(max_workers=16) to parallelize getInfo() across the divided time blocks because getInfo() calls are synchronous and if they are run parallely it would give faster execution.
Filter and select:

```python
ee.ImageCollection(dataset_id)
    .filterDate(start, end)
    .select(parameter_name)
    .mean()
```

Extract value using .reduceRegion() at scale=10000 over:
Following is the correct method to extract the value from here
```python
point = ee.Geometry.Point({lon}, {lat})

value = image.reduceRegion(
    reducer=ee.Reducer.first(),
    geometry=point,
    scale=10000
)
```
Before performing any analysis (like mean, std), you must filter out None values.


Collect each returned value into a list:
According to above value
value.getInfo() gets us the value after reduceRegion is applied
```python
[value1, value2, ..., valueN]
```

Use ThreadPoolExecutor(max_workers=16) to parallelize getInfo() across the divided time blocks
Store the full array of data points as:

```python
data_points[f"{{dataset_id}}_{{parameter_name}}"] = [list of values from getInfo()]
```

✅ You are using ThreadPoolExecutor to parallelize across time blocks, not just across parameters
✅ .getInfo() is synchronous — this bypasses bottlenecks
Before performing any analysis (like mean, std), you must filter out None values.


This means your data_points list contains dictionaries instead of raw numbers. To fix this, you must extract just the numeric value when calling .getInfo().
I DO NOT WANT THE ERROR because you are doing dict + dict I DO NOT WANT THAT
When collecting data from `.getInfo()`, extract only the raw numeric values (e.g., `float`, `int`) into a list.

🔸 When collecting data from `.getInfo()`, **extract only the raw numeric value** for each parameter.
DO NOT store the entire dictionary returned by `.getInfo()` — instead, extract just the value associated with the parameter name.

✅ For example:
```python
value = image.reduceRegion(...).getInfo()
raw_value = value.get(parameter_name)
```

Append `raw_value` to your list of data points.

🔸 The final structure should be:
```python
data_points = {{
  "datasetID_parameterName": [val1, val2, ..., valN]  # each val is float or int, NOT dict
}}
```

🔸 This ensures all statistical functions like `np.mean`, `np.std`, etc., will work without error.


🔹 STEP 4: Statistical Analysis Using Standard Libraries
Dynamically pick the analysis type from input JSON (analysis_type) and only write code for that analysis whichever it may be.
No need to write conditional statements for analysis as you have already determined what analysis you want to conduct.
For the parameters mentioned in the analysis file in the input, conduct the analysis directly.
Below is like a helper context for you to perform data analysis from. But you must write appropriate code for analysis based on the input JSON that you are given.
If the type of analysis is to compare multiple parameters then the emphasis of data analysis must also additionally include the correlation between them using statistics.

Using the raw time series from data_points, apply:

numpy / pandas: mean, std, min, max, rolling, z-score

scipy.stats: correlation, anomaly detection

statsmodels.api: seasonal_decompose, OLS regression

sklearn: linear regression for trend



✅ These must be calculated programmatically
✅ Use the actual GEE values (no fake data)

🔹 STEP 5: Summarize Using Groq

Define:

```python
def get_llm():
    chat = ChatGroq(api_key="{groqq}", model="llama-3.1-8b-instant")
```
Groq will return a plain-text interpretation: summary, anomalies, suggestions and this is the way it will be instantiated.
DO NOT HALLUCINATE OTHER TYPE OF USAGE DIRECTLY USE THIS TYPE AND THE NECESSARY IMPORTS HAVE ALREADY BEEN INCLUDED ABOVE.
Pass a dictionary of all statistics per parameter to Groq like:

in our main() function pass in when access the get_llm invoke the llm such as:
```python
def main():
    llm = get_llm()
    summary_text = llm.invoke("Summarize the following mathematical analysis: " + str(analysis_summary))
    suggestions = llm.invoke("What do the following statistics mean for the end user's according to, instead of using statistical numbers, explain in human understandable format such that they can get valuable insights from the data." + str(summary_text))
```

```json
{{
  "parameter": "NO2",
  "mean": 24.2,
  "std_dev": 3.4,
  "trend_slope": 0.6,
  "seasonality": "weekly",
  "correlation_with_SO2": -0.3
}}
```
These parameters will be generated by our Python analysis code above only



🔹 STEP 6: Final Output Structure

Return a dictionary like:

```python
{{
  "data_points": {{
    "parameter_1": [val1, val2, ...],
    "parameter_1": [val1, val2, ...]
  }},
  "analysis_summary": "<Groq-generated text with findings>"
  "analysis_suggestions" : "<Groq-generated text with findings>"
}}
```

✅ Data comes directly from .getInfo() for each time block
✅ Statistical JSON is computed from these values
✅ Summary is LLM-generated

📌 REMEMBER:


Store raw data per parameter which will be generated by the GEE API and returned in final output under data_points.

"""
    return get_llm().invoke(prompt).content
