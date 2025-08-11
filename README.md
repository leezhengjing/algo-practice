# 🎯 Algorithm Practice Hub

[![Tests](https://github.com/leezhengjing/algo-practice/actions/workflows/run_tests.yml/badge.svg)](https://github.com/leezhengjing/algo-practice/actions/workflows/run_tests.yml)
[![Pages](https://img.shields.io/badge/GitHub%20Pages-Live-blue?logo=github)](https://leezhengjing.github.io/algo-practice/)
[![Languages](https://img.shields.io/badge/Languages-Python%20%7C%20C%2B%2B%20%7C%20JavaScript%20%7C%20TypeScript-brightgreen)](#)

> 🚀 **Live Dashboard**: [View Results & Solutions](https://leezhengjing.github.io/algo-practice/)

Welcome to my algorithm practice repository! This project automatically tests coding solutions across multiple languages and generates a beautiful web dashboard to track progress.

## ✨ Features

- 🔄 **Multi-language Support**: Solutions in Python, C++, JavaScript, and TypeScript
- 🧪 **Automated Testing**: Comprehensive test suite with JSON-based test cases
- 📊 **Live Dashboard**: Interactive web interface with syntax-highlighted code
- 🎨 **Beautiful UI**: Clean, responsive design with status indicators
- ⚡ **CI/CD Pipeline**: Automatic testing and deployment via GitHub Actions
- 📈 **Progress Tracking**: Visual pass/fail status for each problem and language

## 🏗️ Project Structure

```
algo-practice/
├── problems/                    # Problem solutions
│   ├── example/
│   │   ├── attempt.py          # Python solution
│   │   ├── attempt.cpp         # C++ solution
│   │   ├── attempt.js          # JavaScript solution
│   │   ├── attempt.ts          # TypeScript solution
│   │   └── tests.json          # Test cases
│   └── vanilla_binary_search/
│       ├── attempt.py
│       ├── attempt.cpp
│       ├── attempt.js
│       ├── attempt.ts
│       └── tests.json
├── test_runner/                 # Test execution engine
│   ├── main.py                 # Main test runner
│   ├── run_python.py           # Python executor
│   ├── run_cpp.py              # C++ compiler & executor
│   └── run_js.py               # JavaScript executor
└── results/                     # Generated reports
    ├── index.html              # Main dashboard
    ├── {problem}.html          # Individual problem pages
    └── results.json            # Test results data
```

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/leezhengjing/algo-practice.git
   cd algo-practice
   ```

2. **Run tests locally**:
   ```bash
   python3 test_runner/main.py
   ```

3. **View results**:
   ```bash
   open results/index.html
   ```

## 📝 Adding New Problems

1. Create a new folder in `problems/` with your problem name
2. Add your solution files:
   - `attempt.py` (Python)
   - `attempt.cpp` (C++)
   - `attempt.js` (JavaScript)
   - `attempt.ts` (TypeScript)
3. Create `tests.json` with test cases:
   ```json
   {
     "tests": [
       {
         "input": "your input here",
         "output": "expected output"
       }
     ]
   }
   ```

## 🎨 Dashboard Features

- **📋 Overview Table**: Quick status overview for all problems
- **🔍 Detailed Views**: Click any problem to see syntax-highlighted code
- **✅ Status Indicators**: 
  - 🟢 **Pass**: All tests successful
  - 🔴 **Fail**: Some tests failed
  - 🟠 **Missing**: Solution file not found
- **🔗 Easy Navigation**: Links between overview and detailed pages

## 🛠️ Technologies Used

- **Backend**: Python test runners
- **Frontend**: HTML, CSS, JavaScript with Prism.js syntax highlighting
- **CI/CD**: GitHub Actions
- **Deployment**: GitHub Pages

---

<div align="center">

**Happy Coding!** 🎉

Made with ❤️ for algorithm practice

</div>