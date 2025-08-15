import os
import matplotlib.pyplot as plt
from extract_series import extract_parameters_over_reports
import json
import sys

# Reference normal ranges — adjust as needed
NORMAL_RANGES = {
    "Hemoglobin": (13.5, 17.5),
    "LDL": (1.5, 3.5),
    "HDL": (1.0, 1.6),
    "Glucose": (3.5, 5.5),
    "CRP": (0.0, 3.0)
}

def plot_parameters_separately(param_dict):
    normal_dir = os.path.join("plots", "figures", "normal")
    extreme_dir = os.path.join("plots", "figures", "extreme")
    os.makedirs(normal_dir, exist_ok=True)
    os.makedirs(extreme_dir, exist_ok=True)

    for param, values in param_dict.items():
        if all(v == '-' for v in values):
            continue

        numeric_values = [float(v) if v != '-' else None for v in values]
        num_reports = len(numeric_values)
        x = list(range(1, num_reports + 1))

        lower, upper = NORMAL_RANGES.get(param, (None, None))
        if lower is not None and upper is not None:
            is_extreme = any(
                (v is not None) and (v < lower or v > upper)
                for v in numeric_values
            )
        else:
            is_extreme = False

        color = 'red' if is_extreme else 'green'
        save_dir = extreme_dir if is_extreme else normal_dir

        plt.figure(figsize=(8, 5))
        plt.plot(x, numeric_values, marker='o', color=color, label=param)

        # Plot normal boundaries if available
        if lower is not None and upper is not None:
            plt.axhline(y=lower, color='gray', linestyle='--', linewidth=1, label='Lower Bound')
            plt.axhline(y=upper, color='gray', linestyle='--', linewidth=1, label='Upper Bound')

        plt.xlabel("Report Index")
        plt.ylabel("Value")
        plt.title(f"{param} Trend")
        plt.grid(True)
        plt.legend(loc="best")
        plt.tight_layout()

        filename = f"{param.replace(' ', '_')}.png"
        plt.savefig(os.path.join(save_dir, filename))
        plt.close()

if __name__ == "__main__":
    file_path = "report_generator/combined_report_analysis.txt"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = extract_parameters_over_reports(data)
    plot_parameters_separately(result)
