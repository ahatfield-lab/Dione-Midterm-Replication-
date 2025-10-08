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
