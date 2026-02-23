<p align="center">
  <img src="assets/call_me_maybe.png" width="260" />
</p>
<h3 align="center">
  <em>Introduction to function calling in LLMs</em>
</h3>

---

<div align="center">
  <img src="https://img.shields.io/badge/SCORE-None-%235CB338?style=for-the-badge&logo=42&logoColor=white"/>
  <img src="https://img.shields.io/badge/COMPLETED-No-%23007ACC?style=for-the-badge&logo=calendar&logoColor=white"/>
</div>

## ⚠️ Disclaimer

- **Full Portfolio:** This repository focuses on this specific project. You can find my entire 42 curriculum 👉 [here](https://github.com/Overtekk/42).
- **Subject Rules:** I strictly follow the rules regarding 42 subjects; I cannot share the PDFs, but I explain the concepts in this README.
- **Archive State:** The code is preserved exactly as it was during evaluation (graded state). I do not update it, so you can see my progress and mistakes from that time.
- **Academic Integrity:** I encourage you to try the project yourself first. Use this repo only as a reference, not for copy-pasting. Be patient, you will succeed.

---

## ✏️ Quick Start

```bash
todo
```

---

## 📂 Description

A **Large Language Model (LLM)** is an artificial intelligence system trained on massive datasets to process, understand, and generate human language. Technically, it operates as a probabilistic engine that calculates and predicts the most relevant next token based on the provided input context.

### About This Project: Function Calling & Constrained Decoding

Large Language Models (LLMs) excel at understanding natural language but lack the native ability to produce reliable, machine-executable outputs. This project focuses on **Function Calling**, a mechanism that translates user prompts into structured function calls (e.g., JSON formats with typed arguments) to interact with external systems, execute code, and extract data.

**The Technical Challenge:**
While large models can format outputs natively, smaller models (e.g., 0.6B parameters) are notoriously unreliable at generating valid data structures, often failing 70% of the time when prompted for JSON.

**Our Approach:**
To achieve production-grade reliability (99%+), this project implements **Constrained Decoding**. Rather than relying on prompt engineering, this technique controls the model's generation process token-by-token, mathematically guaranteeing a valid structural output.

### 📜 Summary:

This project focuses on building a function calling tool that translates natural language prompts into structured function calls. Given a specific user question *(e.g., "What is the sum of 40 and 2?")*, the system must not answer the question directly, but instead output the appropriate function name and its required arguments formatted as JSON:
```bash
[
	{
	"name": "fn_add_numbers",
	"description": "Add two numbers together and return their sum.",
	"parameters": {
		"a": {
			"type": "number"
		},
		"b": {
			"type": "number"
		}
	},
	"returns": {
		"type": "number"
	}
	}
]
```
The implementation relies on **constrained decoding** to guarantee 100% valid JSON output. This technique modifies the logits before token selection by setting the probabilities of schema-breaking tokens to negative infinity, ensuring reliable outputs even with a small 0.5B parameter model.

The system processes two main input files located in the `data/input/` directory:
* `function_calling_tests.json`: Contains the natural language prompts to evaluate.
* `function_definitions.json`: Defines the available functions, including argument names, types, and descriptions.

The program must generate a single output file named `function_calling_results.json`. Each object within this array must strictly contain the `prompt`, the function `name`, and the `parameters`. The final solution must achieve over 90% accuracy for function selection and process all test prompts in under 5 minutes.

### 📝 Rules:

- Must be written in **Python >=3.10**.
- Must adhere to the **flake8** and **mypy** standard.
- Crash and leaks must be properly managed. All errors must be handled gracefully.
- Code must include type hints and docstrings *[(following PEP 257)](https://peps.python.org/pep-0257/)*
- All classes must use `pydantic` for validation.
- `dspy` (or any similar package) is forbidden including `pytorch`, `huggingface package`, `transformers`, `outlines`, etc.
- The model we need to use for this project must be **Qwen/Qwen3-0.6B** by default. But any other models can be used as long the project works with the mandatory model.
- It's forbidden to use any private methods or attributes from the `llm_sdk` package.
- The function to call should be chosen using the LLM.

### 📮 Makefile:

This project must have a Makefile and the following rules:
- **install**: install project dependencies using **pip**, **uv** etc...
- **run**: execute the main script of the project.
- **debug**: run the main script in debug mode using Python's pdb.
- **clean**: Remove temporary files or caches.
- **lint**: execute the commands `flake8` . and `mypy . --warn-return-any
--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs
--check-untyped-defs`.
- **lint**: execute the commands `flake8 .` and `mypy . --strict`.

---

## 💡 Instructions

### 1. Git clone this repository:
```bash
git clone https://github.com/Overtekk/Call_me_Maybe.git
```

### 2. Run:
```bash
todo
```

### Example of use:

todo

---

## ⚙️ How it works?

### Algorithm:

todo

### Choice of design:

todo

### Performance analysis:

todo

### Challenges faced:

todo

### Testing strategy:

todo

---

## 📚 Resources

todo

---
