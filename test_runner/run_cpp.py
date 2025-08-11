import subprocess
import os

def run_cpp(code_path, test_input):
    exe_path = code_path.replace(".cpp", "")
    try:
        subprocess.run(["g++", code_path, "-o", exe_path], check=True)
        result = subprocess.run(
            [exe_path],
            input=test_input.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=3
        )
        return result.stdout.decode().strip(), result.stderr.decode().strip()
    except subprocess.TimeoutExpired:
        return None, "Timeout"
    except subprocess.CalledProcessError as e:
        return None, f"Compile Error: {e}"
