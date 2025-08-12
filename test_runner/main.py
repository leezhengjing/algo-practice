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

# Walk through all subdirectories in problems/
for root, dirs, files in os.walk("problems"):
    # Skip the root problems directory itself
    if root == "problems":
        continue
    
    # Check if this directory contains tests.json
    tests_path = os.path.join(root, "tests.json")
    if not os.path.exists(tests_path):
        continue
    
    # Get relative path from problems/ for the problem name
    problem_name = os.path.relpath(root, "problems")
    
    with open(tests_path) as f:
        tests_data = json.load(f)
    
    # Skip if no tests (for templates/snippets)
    if not tests_data.get("tests") or len(tests_data["tests"]) == 0:
        continue
    
    results[problem_name] = {}
    
    for ext, runner in LANG_RUNNERS.items():
        code_path = os.path.join(root, f"attempt.{ext}")
        if not os.path.exists(code_path):
            results[problem_name][ext] = "❌ Missing"
            continue
        
        all_passed = True
        for t in tests_data["tests"]:
            output, error = runner(code_path, t["input"])
            if error or output.strip() != t["output"].strip():
                all_passed = False
                break
        results[problem_name][ext] = "✅ Pass" if all_passed else "❌ Fail"

# Save JSON
os.makedirs("results", exist_ok=True)
with open("results/results.json", "w") as f:
    json.dump(results, f, indent=2)

# Organize results by categories
categories = {}
for prob, langs in results.items():
    # Get category from path (first folder or "uncategorized")
    if "/" in prob:
        category = prob.split("/")[0]
        problem_name = "/".join(prob.split("/")[1:])
    else:
        category = "uncategorized"
        problem_name = prob
    
    if category not in categories:
        categories[category] = {}
    categories[category][problem_name] = langs

# Generate HTML with category overview
html_content = """<html>
<head>
    <title>Algorithm Practice Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .category-card { 
            background: white; 
            border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
            margin: 20px 0; 
            padding: 20px;
        }
        .category-header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            border-bottom: 2px solid #eee; 
            padding-bottom: 10px; 
            margin-bottom: 15px;
        }
        .category-title { font-size: 1.5em; font-weight: bold; color: #333; }
        .category-stats { display: flex; gap: 20px; }
        .stat-item { text-align: center; }
        .stat-number { font-size: 1.8em; font-weight: bold; }
        .stat-label { font-size: 0.9em; color: #666; }
        .progress-bar { 
            width: 200px; 
            height: 10px; 
            background: #eee; 
            border-radius: 5px; 
            overflow: hidden;
            margin: 5px 0;
        }
        .progress-fill { 
            height: 100%; 
            background: linear-gradient(90deg, #4CAF50, #45a049); 
            transition: width 0.3s ease;
        }
        .problems-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); 
            gap: 15px; 
            margin-top: 15px;
        }
        .problem-card { 
            background: #f9f9f9; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
            padding: 15px;
        }
        .problem-name { font-weight: bold; margin-bottom: 8px; }
        .problem-languages { display: flex; gap: 10px; }
        .lang-status { 
            padding: 4px 8px; 
            border-radius: 3px; 
            font-size: 0.85em; 
            font-weight: bold;
        }
        .pass { background: #d4edda; color: #155724; }
        .fail { background: #f8d7da; color: #721c24; }
        .missing { background: #fff3cd; color: #856404; }
        .overall-stats { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            border-radius: 10px; 
            padding: 20px; 
            margin-bottom: 30px;
            text-align: center;
        }
        .overall-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; }
        .overall-stat { }
        .overall-number { font-size: 2.5em; font-weight: bold; }
        .overall-label { font-size: 1.1em; opacity: 0.9; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Algorithm Practice Dashboard</h1>
            <p>Track your progress across different problem categories</p>
        </div>"""

# Calculate overall statistics
total_problems = len(results)
total_tests = sum(len([l for l in langs.values() if "Pass" in l or "Fail" in l]) for langs in results.values())
total_passed = sum(len([l for l in langs.values() if "Pass" in l]) for langs in results.values())
total_missing = sum(len([l for l in langs.values() if "Missing" in l]) for langs in results.values())

# Add overall stats
html_content += f"""
        <div class="overall-stats">
            <div class="overall-grid">
                <div class="overall-stat">
                    <div class="overall-number">{total_problems}</div>
                    <div class="overall-label">Total Problems</div>
                </div>
                <div class="overall-stat">
                    <div class="overall-number">{total_passed}</div>
                    <div class="overall-label">Solutions Passing</div>
                </div>
                <div class="overall-stat">
                    <div class="overall-number">{total_tests - total_missing}</div>
                    <div class="overall-label">Solutions Attempted</div>
                </div>
                <div class="overall-stat">
                    <div class="overall-number">{round(total_passed/max(total_tests-total_missing, 1)*100)}%</div>
                    <div class="overall-label">Success Rate</div>
                </div>
            </div>
        </div>"""

# Add category sections
for category, problems in sorted(categories.items()):
    # Calculate category stats
    cat_total = len(problems)
    cat_solutions = sum(len([l for l in langs.values() if "Pass" in l or "Fail" in l]) for langs in problems.values())
    cat_passed = sum(len([l for l in langs.values() if "Pass" in l]) for langs in problems.values())
    cat_missing = sum(len([l for l in langs.values() if "Missing" in l]) for langs in problems.values())
    cat_attempted = cat_solutions
    cat_success_rate = round(cat_passed/max(cat_attempted, 1)*100) if cat_attempted > 0 else 0
    
    # Format category name
    display_category = category.replace("_", " ").title()
    
    html_content += f"""
        <div class="category-card">
            <div class="category-header">
                <div class="category-title">{display_category}</div>
                <div class="category-stats">
                    <div class="stat-item">
                        <div class="stat-number">{cat_total}</div>
                        <div class="stat-label">Problems</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{cat_passed}</div>
                        <div class="stat-label">Passing</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{cat_success_rate}%</div>
                        <div class="stat-label">Success</div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {cat_success_rate}%"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="problems-grid">"""
    
    # Add individual problems in this category
    for prob_name, langs in sorted(problems.items()):
        # Create safe filename for nested paths
        full_prob_name = f"{category}/{prob_name}" if category != "uncategorized" else prob_name
        safe_filename = full_prob_name.replace("/", "_").replace("\\", "_")
        
        html_content += f"""
                <div class="problem-card">
                    <div class="problem-name">
                        <a href="{safe_filename}.html" style="text-decoration: none; color: #333;">{prob_name}</a>
                    </div>
                    <div class="problem-languages">"""
        
        for ext in ["py", "cpp", "js"]:
            lang_short = {"py": "Py", "cpp": "C++", "js": "JS"}[ext]
            status = langs.get(ext, "❌ Missing")
            status_class = "pass" if "Pass" in status else ("fail" if "Fail" in status else "missing")
            status_text = "✓" if "Pass" in status else ("✗" if "Fail" in status else "○")
            
            html_content += f'<span class="lang-status {status_class}">{lang_short} {status_text}</span>'
        
        html_content += """
                    </div>
                </div>"""
    
    html_content += """
            </div>
        </div>"""

html_content += """
    </div>
</body>
</html>"""

# Generate individual problem pages
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
        .back-link {{ margin-bottom: 20px; }}
        .back-link a {{ text-decoration: none; background: #007acc; color: white; padding: 8px 15px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="back-link">
        <a href="index.html">← Back to Dashboard</a>
    </div>
    <h1>{prob}</h1>
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
    # Create safe filename for nested paths
    safe_filename = prob.replace("/", "_").replace("\\", "_")
    with open(f"results/{safe_filename}.html", "w") as f:
        f.write(problem_html)

with open("results/index.html", "w") as f:
    f.write(html_content)