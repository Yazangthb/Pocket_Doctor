import os
import openai
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def read_all_txt_files(directory):
    reports = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                reports[filename] = f.read()
    return reports


def analyze_multiple_blood_reports(report_dict):
    report_blocks = "\n\n".join([f"Report: {name}\n{content}" for name, content in report_dict.items()])

    prompt = f"""
    You are a medical assistant AI. A user has provided multiple blood test reports. Each report is from a different day or individual. 

    Your tasks:
    1. For each report, extract blood parameters and return them in a structured JSON format with field names, values, and units.
    2. For each report, provide a brief medical summary.
    3. At the end, provide ONE unified recommendation for follow-up or next steps, considering all the reports collectively.

    Here are the reports:

    {report_blocks}

    Respond in this JSON format:
    {{
    "reports": [
        {{
        "file": "report1.txt",
        "parameters": [
            {{
            "name": "Hemoglobin",
            "value": 13.2,
            "unit": "g/dL"
            }},
            ...
        ],
        "summary": "Brief summary for this report"
        }},
        ...
    ],
    "overall_follow_up_advice": "Combined advice based on all reports"
    }}
        """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response['choices'][0]['message']['content']


def main(directory="LLM_output", output_path="combined_report_analysis.txt"):
    reports = read_all_txt_files(directory)
    if not reports:
        print(f"No .txt files found in {directory}")
        return

    result = analyze_multiple_blood_reports(reports)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Analysis written to {output_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        main()  # default to LLM_output
    else:
        main(sys.argv[1])
