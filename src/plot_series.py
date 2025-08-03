import matplotlib.pyplot as plt
from extract_series import extract_parameters_over_reports
import json
import sys

def plot_all_parameters_single_chart(param_dict):
    num_reports = len(next(iter(param_dict.values())))
    x = list(range(1, num_reports + 1))

    plt.figure(figsize=(12, 8))

    for param, values in param_dict.items():
        # Skip empty or all-missing values
        if all(v == '-' for v in values):
            continue

        # Convert values to float, replacing '-' with None
        numeric_values = [float(v) if v != '-' else None for v in values]
        plt.plot(x, numeric_values, marker='o', label=param)

    plt.xlabel("Report Index")
    plt.ylabel("Value")
    plt.title("Blood Analysis Parameter Trends Across Reports")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Default file path
    file_path = "combined_report_analysis.txt"

    # Use the provided argument if available
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = extract_parameters_over_reports(data)
    plot_all_parameters_single_chart(result)