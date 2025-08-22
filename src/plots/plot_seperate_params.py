import os
import matplotlib.pyplot as plt
from extract_series import extract_parameters_over_reports
import json
import sys

# Reference normal ranges — adjust as needed (adult ranges)
NORMAL_RANGES = {
    "Hemoglobin": (135, 175),
    "White Blood Cells": (4.0, 10.0),
    "Red Blood Cells": (4.2, 5.9),
    "Platelets": (150, 450),
    "Hematocrit": (38, 50),
    "Mean Corpuscular Volume": (80, 100),
    "Mean Corpuscular Hemoglobin": (27, 33),
    "Mean Corpuscular Hemoglobin Concentration": (32, 36),
    "Red Cell Distribution Width": (11.5, 14.5),
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
        outliers, normals = [], []

        for xi, v in zip(x, numeric_values):
            if v is None:
                continue
            if lower is not None and upper is not None and (v < lower or v > upper):
                outliers.append((xi, v))
            else:
                normals.append((xi, v))

        is_extreme = len(outliers) > 0
        save_dir = extreme_dir if is_extreme else normal_dir

        plt.figure(figsize=(8, 5))

        # Shaded healthy range with annotation
        if lower is not None and upper is not None:
            plt.axhspan(lower, upper, color='lightgreen', alpha=0.25)
            plt.text(
                0.5, (lower + upper) / 2,
                "Healthy range",
                color="green", fontsize=10, alpha=0.8,
                ha="center", va="center",
                transform=plt.gca().get_yaxis_transform()
            )

        # Plot normal values in green
        if normals:
            plt.plot(
                [p[0] for p in normals],
                [p[1] for p in normals],
                marker='o', color='green', linewidth=2, markersize=8
            )

        # Plot outliers in red
        if outliers:
            plt.plot(
                [p[0] for p in outliers],
                [p[1] for p in outliers],
                marker='o', color='red', linewidth=2, markersize=10
            )

        plt.xlabel("Report number")
        plt.ylabel("Value")
        plt.title(f"{param} Trend")
        plt.grid(True, linestyle=":", alpha=0.7)
        plt.tight_layout()

        filename = f"{param.replace(' ', '_')}.png"
        plt.savefig(os.path.join(save_dir, filename))
        plt.close()


if __name__ == "__main__":
    file_path = "report_generator/combined_report_analysis.txt"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = extract_parameters_over_reports(data)
    plot_parameters_separately(result)
