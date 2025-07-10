from e2b import Sandbox

def run_in_sandbox(code: str) -> str:
    with Sandbox(template="python3") as sandbox:
        result = sandbox.filesystem.write("script.py", code)
        output = sandbox.run("python script.py")
        return output.stdout
