import os
import pandas as pd
import csv
import os
import json
os.chdir(os.path.dirname(os.path.abspath(__file__)))

input_root = "paper_data"
output_root = "data"

def process_file(input_file, output_tsv, output_jsonl):
    sentences = []
    labels = []
    sentence = []
    targets = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                if sentence:
                    sentences.append(sentence.copy())     
                    labels.append(targets.copy())       
                    sentence, targets = [], []
            else:
                word, tag = line.split()
                sentence.append(word)
                targets.append(tag)

    if sentence:
        sentences.append(sentence.copy())
        labels.append(targets.copy())

    # Save TSV 
    df = pd.DataFrame({"text": [" ".join(s) for s in sentences],
                       "target": [" ".join(t) for t in labels]})
    df.insert(0, "textid", range(1, len(df) + 1))
    os.makedirs(os.path.dirname(output_tsv), exist_ok=True)
    df.to_csv(output_tsv, sep="\t", index=False, quoting=csv.QUOTE_NONE, escapechar="\\")

    # Save JSONL
    with open(output_jsonl, "w", encoding="utf-8") as f:
        for tokens, tags in zip(sentences, labels):
            f.write(json.dumps({"tokens": tokens, "tags": tags}, ensure_ascii=False) + "\n")

    print(f"Saved: {output_tsv} and {output_jsonl}")

# Walk through all language folders
for lang in os.listdir(input_root):
    lang_path = os.path.join(input_root, lang)
    if os.path.isdir(lang_path):
        for split in ["train.txt", "dev.txt", "test.txt"]:
            input_file = os.path.join(lang_path, split)
            if os.path.exists(input_file):
                output_tsv = os.path.join(output_root, lang, f"processed_{split.replace('.txt','.tsv')}")
                output_jsonl = os.path.join(output_root, lang, f"processed_{split.replace('.txt','.jsonl')}")
                process_file(input_file, output_tsv, output_jsonl)

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

def write_jsonl(df, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            tokens = row["text"].split()
            tags = row["target"].split()
            f.write(json.dumps({"tokens": tokens, "tags": tags}, ensure_ascii=False) + "\n")

if all_train_dfs:
    combined_train = pd.concat(all_train_dfs, ignore_index=True)
    os.makedirs(os.path.join(output_root, "all_languages"), exist_ok=True)
    write_jsonl(combined_train, os.path.join(output_root, "all_languages/train.jsonl"))
    print("Saved: train.jsonl")

if all_dev_dfs:
    combined_dev = pd.concat(all_dev_dfs, ignore_index=True)
    write_jsonl(combined_dev, os.path.join(output_root, "all_languages/dev.jsonl"))
    print("Saved: dev.jsonl")

if all_test_dfs:
    combined_test = pd.concat(all_test_dfs, ignore_index=True)
    combined_test.to_csv(os.path.join(output_root, "all_languages/test.tsv"), sep="\t", index=False, quoting=csv.QUOTE_NONE, escapechar="\\")
    print("Saved: test.tsv")
