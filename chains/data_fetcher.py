from chains.code_generator import generate_gee_code
from utils.sandbox_runner import run_in_sandbox

def fetch_data_from_gee(region, start, end, dataset):
    code = generate_gee_code(region, start, end, dataset)
    result = run_in_sandbox(code)
    with open("output/gee_output.json", "w") as f:
        f.write(result)
    return result
