import json
import os
from run_python import run_python
from run_cpp import run_cpp
from run_js import run_js

LANG_RUNNERS = {
    "py": run_python,
    "cpp": run_cpp,
    "js": run_js
}

results = {}

for problem in os.listdir("problems"):
    problem_path = os.path.join("problems", problem)
    if not os.path.isdir(problem_path):
        continue
    
    tests_path = os.path.join(problem_path, "tests.json")
    if not os.path.exists(tests_path):
        continue
    
    with open(tests_path) as f:
        tests = json.load(f)
    
    results[problem] = {}
    
    for ext, runner in LANG_RUNNERS.items():
        code_path = os.path.join(problem_path, f"attempt.{ext}")
        if not os.path.exists(code_path):
            results[problem][ext] = "❌ Missing"
            continue
        
        all_passed = True
        for t in tests:
            output, error = runner(code_path, t["input"])
            if error or output.strip() != t["output"].strip():
                all_passed = False
                break
        results[problem][ext] = "✅ Pass" if all_passed else "❌ Fail"

# Save JSON
os.makedirs("results", exist_ok=True)
with open("results/results.json", "w") as f:
    json.dump(results, f, indent=2)

# Generate HTML
html = "<html><head><title>Test Results</title></head><body><h1>Test Results</h1><table border='1'><tr><th>Problem</th><th>Python</th><th>C++</th><th>JS</th></tr>"
for prob, langs in results.items():
    html += f"<tr><td>{prob}</td><td>{langs.get('py','-')}</td><td>{langs.get('cpp','-')}</td><td>{langs.get('js','-')}</td></tr>"
html += "</table></body></html>"

with open("results/index.html", "w") as f:
    f.write(html)
