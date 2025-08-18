import os
import json
import matplotlib.pyplot as plt

def extract_health_scores_from_dir(directory):
    scores = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "general_health_score" in data:
                    scores.append(int(round(data["general_health_score"])))
            except json.JSONDecodeError as e:
                print(f"⚠️ Skipping {filename} (invalid JSON): {e}")
    
    return scores

def plot_scores_with_trends(scores, save_path="plots/figures/general_health_scores_all.png"):
    if not scores:
        print("No valid scores found.")
        return

    plt.figure(figsize=(len(scores) * 1.2, 2))  # wide figure for horizontal layout
    plt.axis("off")
    plt.title("General Health Scores", fontsize=16, pad=20)

    for i, score in enumerate(scores):
        prev = scores[i-1] if i > 0 else score
        if score > prev:
            arrow, color = "↑", "green"
        elif score < prev:
            arrow, color = "↓", "red"
        else:
            arrow, color = "→", "gray"

        plt.text((i+1)/(len(scores)+1), 0.5, 
                 f"{score} {arrow}",
                 fontsize=20, ha="center", va="center", color=color)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    dir_path = "report_generator/reports/"  
    scores = extract_health_scores_from_dir(dir_path)
    print("Extracted Scores:", scores)
    plot_scores_with_trends(scores)
