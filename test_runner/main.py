import json
import os
import html
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
        tests_data = json.load(f)
    
    # Skip if no tests (for templates/snippets)
    if not tests_data.get("tests") or len(tests_data["tests"]) == 0:
        continue
    
    results[problem] = {}
    
    for ext, runner in LANG_RUNNERS.items():
        code_path = os.path.join(problem_path, f"attempt.{ext}")
        if not os.path.exists(code_path):
            results[problem][ext] = "❌ Missing"
            continue
        
        all_passed = True
        for t in tests_data["tests"]:
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
html_content = """<html>
<head>
    <title>Test Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .pass { color: green; }
        .fail { color: red; }
        .missing { color: orange; }
    </style>
</head>
<body>
    <h1>Algorithm Practice - Test Results</h1>
    <table>
        <tr><th>Problem</th><th>Python</th><th>C++</th><th>JavaScript</th><th>Details</th></tr>"""

for prob, langs in results.items():
    # Create individual problem page
    problem_html = f"""<html>
<head>
    <title>{prob} - Solutions</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .code-section {{ margin: 20px 0; }}
        .code-header {{ background-color: #f0f0f0; padding: 10px; border-left: 4px solid #007acc; }}
        pre {{ background-color: #f8f8f8; padding: 15px; border-radius: 5px; overflow-x: auto; margin: 0; }}
        pre code {{ background: none; }}
        .status {{ font-weight: bold; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
        .missing {{ color: orange; }}
    </style>
</head>
<body>
    <h1>{prob}</h1>
    <p><a href="index.html">← Back to Results</a></p>
"""
    
    # Add code sections for each language
    for ext in ["py", "cpp", "js"]:
        lang_name = {"py": "Python", "cpp": "C++", "js": "JavaScript"}[ext]
        prism_lang = {"py": "python", "cpp": "cpp", "js": "javascript"}[ext]
        status = langs.get(ext, "❌ Missing")
        status_class = "pass" if "Pass" in status else ("fail" if "Fail" in status else "missing")
        
        problem_html += f"""
    <div class="code-section">
        <div class="code-header">
            <h3>{lang_name} Solution - <span class="status {status_class}">{status}</span></h3>
        </div>"""
        
        code_path = os.path.join("problems", prob, f"attempt.{ext}")
        if os.path.exists(code_path):
            try:
                with open(code_path, 'r') as f:
                    code_content = f.read()
                escaped_code = html.escape(code_content)
                problem_html += f'<pre><code class="language-{prism_lang}">{escaped_code}</code></pre>'
            except Exception as e:
                problem_html += f"<p>Error reading file: {e}</p>"
        else:
            problem_html += "<p>No solution file found.</p>"
        
        problem_html += "</div>"
    
    problem_html += """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>"""
    
    # Save individual problem page
    with open(f"results/{prob}.html", "w") as f:
        f.write(problem_html)
    
    # Add row to main table with link
    html_content += f"""
        <tr>
            <td><a href="{prob}.html">{prob}</a></td>
            <td class="{'pass' if 'Pass' in langs.get('py', '') else ('fail' if 'Fail' in langs.get('py', '') else 'missing')}">{langs.get('py','-')}</td>
            <td class="{'pass' if 'Pass' in langs.get('cpp', '') else ('fail' if 'Fail' in langs.get('cpp', '') else 'missing')}">{langs.get('cpp','-')}</td>
            <td class="{'pass' if 'Pass' in langs.get('js', '') else ('fail' if 'Fail' in langs.get('js', '') else 'missing')}">{langs.get('js','-')}</td>
            <td><a href="{prob}.html">View Code</a></td>
        </tr>"""

html_content += """
    </table>
</body>
</html>"""

with open("results/index.html", "w") as f:
    f.write(html_content)