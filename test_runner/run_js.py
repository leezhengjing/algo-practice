import subprocess

def run_js(code_path, test_input):
    try:
        result = subprocess.run(
            ["node", code_path],
            input=test_input.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=3
        )
        return result.stdout.decode().strip(), result.stderr.decode().strip()
    except subprocess.TimeoutExpired:
        return None, "Timeout"