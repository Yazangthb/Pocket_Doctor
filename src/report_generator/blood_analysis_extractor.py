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
    "Hemoglobin": {"mean": 135.0, "sd": 7.0, "unit": "g/L"},
    "White Blood Cells": {"mean": 6.6, "sd": 1.3, "unit": "10^9/L"},
    "Red Blood Cells": {"mean": 4.35, "sd": 0.25, "unit": "10^12/L"},
    "Platelets": {"mean": 272.5, "sd": 57.0, "unit": "10^9/L"},
    "Hematocrit": {"mean": 39.5, "sd": 2.4, "unit": "%"},
    "Mean Corpuscular Volume": {"mean": 90.7, "sd": 4.7, "unit": "fL"},
    "Mean Corpuscular Hemoglobin": {"mean": 29.8, "sd": 1.9, "unit": "pg"},
    "Mean Corpuscular Hemoglobin Concentration": {"mean": 322.0, "sd": 8.0, "unit": "g/L"},
    "Red Cell Distribution Width": {"mean": 13.4, "sd": 1.1, "unit": "%"},
    "Blasts": {"mean": 0.0, "sd": 0.0, "unit": "%"},
    "Promyelocytes": {"mean": 0.0, "sd": 0.0, "unit": "%"},
    "Myelocytes": {"mean": 0.0, "sd": 0.0, "unit": "%"},
    "Metamyelocytes": {"mean": 0.0, "sd": 0.0, "unit": "%"},
    "Band Neutrophils": {"mean": 3.0, "sd": 1.0, "unit": "%"},
    "Segmented Neutrophils": {"mean": 55.5, "sd": 7.0, "unit": "%"},
    "Lymphocytes": {"mean": 33.5, "sd": 6.7, "unit": "%"},
    "Monocytes": {"mean": 7.5, "sd": 1.8, "unit": "%"},
    "Eosinophils": {"mean": 5.0, "sd": 2.5, "unit": "%"},
    "Basophils": {"mean": 1.0, "sd": 0.5, "unit": "%"},
    "Plasma Cells": {"mean": 0.0, "sd": 0.0, "unit": "%"},
    "Absolute Neutrophils": {"mean": 3.91, "sd": 1.1, "unit": "10^9/L"},
    "Absolute Lymphocytes": {"mean": 2.27, "sd": 0.44, "unit": "10^9/L"},
    "Absolute Monocytes": {"mean": 0.48, "sd": 0.12, "unit": "10^9/L"},
    "Absolute Eosinophils": {"mean": 0.30, "sd": 0.15, "unit": "10^9/L"},
    "Absolute Basophils": {"mean": 0.045, "sd": 0.02, "unit": "10^9/L"},
    "Mean Platelet Volume": {"mean": 10.8, "sd": 0.6, "unit": "fL"},
    "ESR": {"mean": 15.0, "sd": 7.5, "unit": "mm/h"},
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
            sd = info["sd"]
            if sd == 0:  # avoid division by zero
                continue
            z = abs((val - info["mean"]) / sd)
            scores.append(z)
    if not scores:
        return None
    avg_abs_z = sum(scores) / len(scores)
    health_score = max(0, 100 - avg_abs_z * 10)
    return round(health_score, 1)


def analyze_blood_report(text):
    # Build mapping of expected units from NORMAL_RANGES
    expected_units = {name: info["unit"] for name, info in NORMAL_RANGES.items()}

    unit_instructions = "\n".join([
        f"- {name}: always report in {unit}"
        for name, unit in expected_units.items()
    ])
    print(unit_instructions)
    prompt = f"""
        You are a medical assistant AI.
        The user has provided a blood test report that may be written in Russian.

        Your job is to extract and normalize the data.

        Tasks:
        1. Extract all blood analysis parameters into JSON with English field names.
        2. For each parameter, convert and output the value in the expected unit system.
        Use ONLY these units (convert if necessary):
        {unit_instructions}
        3. Extract the date of the report (if present).
        4. Extract the gender of the patient (if present).
        5. Summarize the likely medical situation (e.g., anemia, infection, normal).
        6. Suggest when the patient should schedule a follow-up.

        Respond ONLY in valid JSON with this format:
        {{
        "report_date": "YYYY-MM-DD or null",
        "gender": "Male/Female/Unknown",
        "parameters": [
            {{ "name": "Hemoglobin", "value": 135, "unit": "g/L" }},
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
