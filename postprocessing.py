import os
import pandas as pd

base_dir = "/Users/huxiyan/Desktop/H/25Fall/COSC426/Dione-Midterm-Replication-/results"
output_csv = os.path.join(base_dir, "summary_accuracy.csv")

rows = []

for model_name in os.listdir(base_dir):
    model_path = os.path.join(base_dir, model_name)
    if not os.path.isdir(model_path):
        continue

    for file_name in os.listdir(model_path):
        if not file_name.endswith(".tsv"):
            continue

        file_path = os.path.join(model_path, file_name)

        parts = file_name.replace("_results_bycond.tsv", "").split("_")
        if len(parts) == 2:
            train_lang, test_lang = parts
        else:
            train_lang, test_lang = "unknown", "unknown"

        df = pd.read_csv(file_path, sep="\t")

        if  "accuracy" not in df.columns:
            print(f"Skipping {file_path}, missing expected columns.")
            continue

        accuracy = df["accuracy"].iloc[0]

        rows.append({
            "Model": model_name,
            "Train_Lang": train_lang,
            "Test_Lang": test_lang,
            "Accuracy": accuracy
        })

summary_df = pd.DataFrame(rows)

summary_df.to_csv(output_csv, index=False)

print(f"Summary table saved to {output_csv}")
print(summary_df)

# To Latex table
input_csv = output_csv
output_txt = os.path.join(base_dir, "summary_accuracy_table.txt")

df = pd.read_csv(input_csv)

train_lang_labels = {
    "fon": "Fon",
    "all": "Combined four languages",
}

test_langs = sorted(df["Test_Lang"].unique())

models = df["Model"].unique()

lines = []
header = "Model & Train Data & " + " & ".join(test_langs) + " \\\\"
lines.append(header)
lines.append("\\hline")

for model in models:
    model_df = df[df["Model"] == model]
    
    train_conditions = [
        ("target", "Target language"),
        ("fon", train_lang_labels.get("fon")),
        ("all", train_lang_labels.get("all"))
    ]

    for i, (cond_key, display_train) in enumerate(train_conditions):
        if cond_key == "target":
            # Select rows where train_lang == test_lang
            sub_df = model_df[model_df["Train_Lang"] == model_df["Test_Lang"]]
        else:
            sub_df = model_df[model_df["Train_Lang"] == cond_key]

        if display_train is None:
            display_train = cond_key.capitalize()

        accuracies = []
        for test_lang in test_langs:
            match = sub_df[sub_df["Test_Lang"] == test_lang]
            if not match.empty:
                accuracies.append(f"{match['Accuracy'].iloc[0]:.3f}")
            else:
                accuracies.append("-")

        model_display = model if i == 0 else ""
        line = f"{model_display:<15} & {display_train:<30} & " + " & ".join(accuracies) + " \\\\"
        lines.append(line)

with open(output_txt, "w") as f:
    f.write("\n".join(lines))

print(f"\n LaTeX table saved to {output_txt}")