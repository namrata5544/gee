from e2b_code_interpreter import Sandbox
import os

def execute_gee_code(generated_code):
    api_key = os.getenv("E2B_API_KEY")
    template_id = "eiub05885v0yzlftpbl0"
    sbx = Sandbox(api_key=api_key, template=template_id)
    
    if "```python" in generated_code:
        code = generated_code.split("```python")[1].split("```")[0]
    else:
        code = generated_code
    
    print("\nExecuting code in sandbox...")
    execution = sbx.run_code(code)
    
    stdout = execution.logs.stdout[0] if execution.logs.stdout else ""
    
    return execution 