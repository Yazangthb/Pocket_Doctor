import os
import json
import matplotlib.pyplot as plt

def extract_health_scores_from_dir(directory):
    scores = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "general_health_score" in data:
                    scores.append(data["general_health_score"])
    
    return scores

def plot_scores(scores, save_path="plots/figures/general_health_scores.png"):
    plt.figure(figsize=(8, 5))
    plt.plot(scores, marker='o', linestyle='-', color='b')
    plt.title("General Health Scores")
    plt.xlabel("Sample Index")
    plt.ylabel("General Health Score")
    plt.grid(True)
    plt.savefig(save_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    dir_path = "report_generator/reports/"  
    scores = extract_health_scores_from_dir(dir_path)
    print("Extracted Scores:", scores)
    plot_scores(scores)
