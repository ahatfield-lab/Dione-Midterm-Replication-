# Dione-Midterm-Replication
This repository contains the code and data necessary to replicate some of the experiments from the paper "MasakhaPOS: Part-of-Speech Tagging for Typologically Diverse African
Languages" by Dione et al. The project focuses on training and evaluating multilingual and Afro-centric language model on various datasets.

## Repository Structure

```
Dione-Midterm-Replication-/
├── data/                      # Dataset files and preprocessing scripts
│   ├── ibo/                    
│   ├── kin/                   
│   ├── sna/                   
│   ├── fon/                   
│   └── all_languages          
├── paper_data/                # Original txt dataset files
├── results/                    
│   ├── XLM-R/                  
│   ├── AfroLM/                
│   ├── figures/               
│   └── tables/
├── data_processing.py
├── data_postprocessing.ipynb               
└── README.md                 # This file
```

## Models
This replication includes:
- Multilingual model:XLM-R
- Afro-centric models: AfroLM
