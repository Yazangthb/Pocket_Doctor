import json

def extract_parameters_over_reports(data):
    reports = data["reports"]

    # Collect all unique parameter names
    all_param_names = set()
    for report in reports:
        for param in report.get("parameters", []):
            all_param_names.add(param["name"])

    # Initialize result dictionary
    result = {param_name: [] for param_name in all_param_names}

    # Fill values or "-" for each report
    for report in reports:
        report_params = {param["name"]: param["value"] for param in report.get("parameters", [])}
        for param_name in all_param_names:
            result[param_name].append(report_params.get(param_name, "-"))

    return result

def main(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    result = extract_parameters_over_reports(data)
    print(result)

# Example usage
if __name__ == "__main__":
    file_path = "combined_report_analysis.txt"  # Change this to your actual file path
    main(file_path)
