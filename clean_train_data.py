import os
import pandas as pd
import csv

input_root = "paper_data"
output_root = "data"

def process_file(input_file, output_file):
    sentences = []
    labels = []
    sentence = []
    targets = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:  
                if sentence:  
                    sentences.append(" ".join(sentence))
                    labels.append(" ".join(targets))
                    sentence, targets = [], []
            else:
                word, tag = line.split()
                sentence.append(word)
                targets.append(tag)

    # Catch last sentence
    if sentence:
        sentences.append(" ".join(sentence))
        labels.append(" ".join(targets))

    # Build dataframe
    df = pd.DataFrame({
        "textid": range(1, len(sentences) + 1),
        "text": sentences,
        "target": labels
    })

    # Save
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, sep="\t", index=False, quoting=csv.QUOTE_NONE, escapechar="\\")

    print(f"Saved: {output_file}")

# Walk through all language folders
for lang in os.listdir(input_root):
    lang_path = os.path.join(input_root, lang)
    if os.path.isdir(lang_path):
        for split in ["train.txt", "dev.txt", "test.txt"]:
            input_file = os.path.join(lang_path, split)
            if os.path.exists(input_file):
                output_file = os.path.join(output_root, lang, f"processed_{split.replace('.txt','.tsv')}")
                process_file(input_file, output_file)

# Create combined files
all_train_dfs = []
all_test_dfs = []
all_dev_dfs = []

for lang in os.listdir(input_root):
    lang_path = os.path.join(input_root, lang)
    if os.path.isdir(lang_path):
        train_file = os.path.join(lang_path, "train.txt")
        dev_file = os.path.join(lang_path, "dev.txt")
        test_file = os.path.join(lang_path, "test.txt")
        if os.path.exists(train_file):
            df_train = pd.read_csv(os.path.join(output_root, lang, "processed_train.tsv"), sep="\t")
            df_train["condition"] = lang
            all_train_dfs.append(df_train)
        if os.path.exists(test_file):
            df_test = pd.read_csv(os.path.join(output_root, lang, "processed_test.tsv"), sep="\t")
            df_test["condition"] = lang
            all_test_dfs.append(df_test)
        if os.path.exists(dev_file):
            df_dev = pd.read_csv(os.path.join(output_root, lang, "processed_dev.tsv"), sep="\t")
            df_dev["condition"] = lang
            all_dev_dfs.append(df_dev)
            
if all_train_dfs:
    combined_train = pd.concat(all_train_dfs, ignore_index=True)
    combined_train.to_csv(os.path.join(output_root, "all_languages/train.tsv"), sep="\t", index=False, quoting=csv.QUOTE_NONE, escapechar="\\")
    print("Saved: train.tsv")
if all_test_dfs:
    combined_test = pd.concat(all_test_dfs, ignore_index=True)
    combined_test.to_csv(os.path.join(output_root, "all_languages/test.tsv"), sep="\t", index=False, quoting=csv.QUOTE_NONE, escapechar="\\")
    print("Saved: test.tsv")
if all_dev_dfs:
    combined_dev = pd.concat(all_dev_dfs, ignore_index=True)
    combined_dev.to_csv(os.path.join(output_root, "all_languages/dev.tsv"), sep="\t", index=False, quoting=csv.QUOTE_NONE, escapechar="\\")
    print("Saved: dev.tsv")