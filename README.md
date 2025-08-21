# 1C_OCR for document Parsing

A docuemnt parsing system for integration with 1C services

## Installation

```bash
git clone https://github.com/Yazangthb/Document_Parsing.git
cd 1c_ocr
conda env create -f environment.yml
conda activate <env-name>
```
## How to  Run

1. Prepare your images in images src/images dir
2. run the script after modifying paths in main.py
```bash
   cd src
   python ocr/main.py
```


## Running LLM Analysis on a Single Report

After obtaining the OCR output, you can analyze it using an LLM to extract structured insights:

```bash
cd src
python report_generator/blood_analysis_extractor.py path/to/ocr_output.txt
```

## Running Multi-Report Analysis

To perform analysis on multiple reports and optionally specify a directory of LLM output `.txt` files:

```bash
cd src
python report_generator/mutli_blood_analysis.py [optional_path/to/dir_with_LLM_output_txt_files]
```

If no directory is provided, the default one will be used.

## Plotting Trends for Report Values

To visualize trends in values across multiple reports:

```bash
cd src
python plots/plot_seperate_params.py
```

This will generate plots in dirs "plots/figures/normal or extreme" showing the changes in various blood test parameters over time.

To visualize trends in general health score across reports:

```bash
cd src
python plots/plot_health_score.py
```

This will generate a time based plot on the general health score.

