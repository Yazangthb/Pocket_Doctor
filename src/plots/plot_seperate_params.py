import os
import matplotlib.pyplot as plt
from extract_series import extract_parameters_over_reports
import json
import sys
from datetime import datetime

# Reference normal ranges — now sex-specific where relevant
NORMAL_RANGES = {
    "Hemoglobin": {
        "Male": (130, 170),
        "Female": (120, 150)
    },
    "White Blood Cells": (3.89, 9.23),  # 10^9/л
    "Red Blood Cells": {
        "Male": (4.3, 5.7),
        "Female": (3.8, 5.1)
    },
    "Platelets": (158, 387),  # 10^9/л
    "Hematocrit": {
        "Male": (40, 50),
        "Female": (36, 46)
    },
    "Mean Corpuscular Volume": (81.3, 100.1),  # фл
    "Mean Corpuscular Hemoglobin": (26.0, 33.6),  # пг
    "Mean Corpuscular Hemoglobin Concentration": (306, 338),  # г/л
    "Red Cell Distribution Width": (11.2, 15.6),  # %
    "Blasts": (0, 0),  # %
    "Promyelocytes": (0, 0),  # %
    "Myelocytes": (0, 0),  # %
    "Metamyelocytes": (0, 0),  # %
    "Band Neutrophils": (1, 5),  # %
    "Segmented Neutrophils": (41, 70),  # %
    "Lymphocytes": (20, 47),  # %
    "Monocytes": (4, 11),  # %
    "Eosinophils": (0, 10),  # %
    "Basophils": (0, 2),  # %
    "Plasma Cells": (0, 0),  # %
    "Absolute Neutrophils": (1.78, 6.04),  # 10^9/л
    "Absolute Lymphocytes": (1.39, 3.15),  # 10^9/л
    "Absolute Monocytes": (0.24, 0.72),  # 10^9/л
    "Absolute Eosinophils": (0.01, 0.59),  # 10^9/л
    "Absolute Basophils": (0.00, 0.09),  # 10^9/л
    "Mean Platelet Volume": (9.6, 12.0),  # фл
    "ESR": {
        "Male": (0, 15),
        "Female": (0, 20)
    },
    "LDL": (1.5, 3.5),  # mmol/L
    "HDL": (1.0, 1.6),  # mmol/L
    "Glucose": (3.5, 5.5),  # mmol/L
    "CRP": (0.0, 3.0)  # mg/L
}


def get_range(param, gender):
    """Return correct normal range depending on gender, if applicable."""
    rng = NORMAL_RANGES.get(param)
    if rng is None:
        return None, None
    if isinstance(rng, dict):
        return rng.get(gender, rng.get("Female"))  # default fallback female if unknown
    return rng


def plot_parameters_separately(param_dict, dates, genders):
    normal_dir = os.path.join("plots", "figures", "normal")
    extreme_dir = os.path.join("plots", "figures", "extreme")
    os.makedirs(normal_dir, exist_ok=True)
    os.makedirs(extreme_dir, exist_ok=True)

    # Convert dates to datetime objects for plotting
    parsed_dates = []
    for d in dates:
        try:
            parsed_dates.append(datetime.strptime(d, "%Y-%m-%d"))
        except Exception:
            parsed_dates.append(None)

    for param, values in param_dict.items():
        if all(v == '-' for v in values):
            continue

        numeric_values = [float(v) if v != '-' else None for v in values]

        outliers, normals = [], []

        for dt, v, g in zip(parsed_dates, numeric_values, genders):
            if v is None or dt is None:
                continue
            lower, upper = get_range(param, g)
            if lower is not None and upper is not None and (v < lower or v > upper):
                outliers.append((dt, v))
            else:
                normals.append((dt, v))

        is_extreme = len(outliers) > 0
        save_dir = extreme_dir if is_extreme else normal_dir

        plt.figure(figsize=(9, 5))

        # Draw reference range for the **most recent gender** (for visualization only)
        if genders and genders[-1] is not None:
            lower, upper = get_range(param, genders[-1])
            if lower is not None and upper is not None:
                plt.axhspan(lower, upper, color='lightgreen', alpha=0.25)
                plt.text(
                    0.5, (lower + upper) / 2,
                    f"Healthy range ({genders[-1]})",
                    color="green", fontsize=10, alpha=0.8,
                    ha="center", va="center",
                    transform=plt.gca().get_yaxis_transform()
                )

        if normals:
            plt.plot(
                [p[0] for p in normals],
                [p[1] for p in normals],
                marker='o', color='green', linewidth=2, markersize=8
            )

        if outliers:
            plt.plot(
                [p[0] for p in outliers],
                [p[1] for p in outliers],
                marker='o', color='red', linewidth=2, markersize=10
            )

        plt.xlabel("Report Date")
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

    # get extracted parameter values
    result = extract_parameters_over_reports(data)

    # get report dates and genders (ordered as in JSON)
    dates = [r.get("report_date") for r in data.get("reports", [])]
    genders = [r.get("gender", "Unknown") for r in data.get("reports", [])]

    plot_parameters_separately(result, dates, genders)
