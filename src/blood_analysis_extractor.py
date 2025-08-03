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

def analyze_blood_report(text):
    prompt = f"""
You are a medical assistant AI. A user has provided a blood test report. 

Your tasks:
1. Extract all available blood analysis parameters and return them as structured JSON with field names, values, and units.
2. Based on the values, describe the likely medical situation of the user (e.g., anemia, infection, normal, etc.).
3. Suggest when they should schedule a second appointment or blood analysis follow-up.

Here is the report:
{text}

Respond in this JSON format:
{{
  "parameters": [
    {{
      "name": "Hemoglobin",
      "value": 13.2,
      "unit": "g/dL"
    }},
    ...
  ],
  "summary": "Brief summary of the user's likely situation.",
  "follow_up_advice": "When and why the user should get another test."
}}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response['choices'][0]['message']['content']

def main(input_path_or_text, output_path="output.txt"):
    text = read_text_input(input_path_or_text)
    result = analyze_blood_report(text)
    
    # Save result to a .txt file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python blood_analysis_extractor.py <path_to_txt_or_text>")
    else:
        main(sys.argv[1], "LLM_output/report_analysis.txt")
