import os
import openai
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_text_input(path_or_text):
    if os.path.exists(path_or_text):
        with open(path_or_text, 'r', encoding='utf-8') as f:
            return f.read()
    return path_or_text  # Assume direct text

import os
import openai
from dotenv import load_dotenv
import json
import math

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Reference norms: replace with actual clinical values
NORMAL_RANGES = {
    "Hemoglobin": {"mean": 14.0, "sd": 1.0, "unit": "g/dL"},
    "LDL": {"mean": 2.5, "sd": 0.8, "unit": "mmol/L"},
    "HDL": {"mean": 1.3, "sd": 0.3, "unit": "mmol/L"},
    "Glucose": {"mean": 5.0, "sd": 0.5, "unit": "mmol/L"},
    "CRP": {"mean": 1.0, "sd": 0.5, "unit": "mg/L"},
}

def compute_health_score(parameters):
    scores = []
    for p in parameters:
        name = p["name"]
        val = p["value"]
        info = NORMAL_RANGES.get(name)
        if info:
            z = abs((val - info["mean"]) / info["sd"])
            scores.append(z)
    if not scores:
        return None
    avg_abs_z = sum(scores) / len(scores)
    health_score = max(0, 100 - avg_abs_z * 10)
    return round(health_score, 1)

def analyze_blood_report(text):
    prompt = f"""
You are a medical assistant AI. A user has provided a blood test report. 

Tasks:
1. Extract blood analysis parameters with names, values, and units into JSON.
2. Assess medical situation (e.g., anemia, infection, normal).
3. Suggest follow-up timing.
Respond in JSON:
{{
  "parameters": [
    {{ "name": "Hemoglobin", "value": 13.2, "unit": "g/dL" }},
    ...
  ],
  "summary": "...",
  "follow_up_advice": "..."
}}
"""
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return json.loads(res['choices'][0]['message']['content'])

def main(input_path_or_text, output_path="output.txt"):
    text = read_text_input(input_path_or_text)
    result = analyze_blood_report(text)
    health_score = compute_health_score(result.get("parameters", []))
    result["general_health_score"] = health_score
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(result, indent=2))

# ... read_text_input ... same as before ...


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python blood_analysis_extractor.py <path_to_txt_or_text>")
    else:
        main(sys.argv[1], "LLM_output/report_analysis1.txt")
