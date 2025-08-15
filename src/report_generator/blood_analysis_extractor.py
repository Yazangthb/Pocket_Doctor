import os
import openai
from dotenv import load_dotenv
import json
import math

# Load API key
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

def read_text_input(path_or_text):
    if os.path.exists(path_or_text):
        with open(path_or_text, 'r', encoding='utf-8') as f:
            return f.read()
    return path_or_text  # Assume direct text

def normalize_value(name, value, unit):
    if name == "Hemoglobin" and unit.lower() == "g/l":
        return value / 10.0, "g/dL"
    return value, unit

def compute_health_score(parameters):
    scores = []
    for p in parameters:
        name = p["name"]
        val, unit = normalize_value(name, p["value"], p["unit"])
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
You are a medical assistant AI.
The user has provided a blood test report that may be written in Russian.
Translate any medical terms or parameter names into English, but keep original numeric values and units.
Perform the analysis as if the report were in English.



Tasks:
1. Extract all blood analysis parameters into JSON with English field names, original numeric values, and units.
2. Summarize the likely medical situation (e.g., anemia, infection, normal).
3. Suggest when the patient should schedule a follow-up.

Respond ONLY in valid JSON with this format:
{{
  "parameters": [
    {{ "name": "Hemoglobin", "value": 13.2, "unit": "g/dL" }},
    ...
  ],
  "summary": "Your summary in English"
}}

Here is the report:
{text}

"""
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    content = res['choices'][0]['message']['content']
    # print("DEBUG RAW RESPONSE:\n", content)

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model did not return valid JSON. Error: {e}\nResponse:\n{content}")

def main(input_path_or_text, output_path="output.txt"):
    text = read_text_input(input_path_or_text)
    result = analyze_blood_report(text)
    health_score = compute_health_score(result.get("parameters", []))
    result["general_health_score"] = health_score
    print(result)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python blood_analysis_extractor.py <path_to_txt_or_text>")
    else:
        main(sys.argv[1], "report_generator/reports/report_analysis2.txt")
