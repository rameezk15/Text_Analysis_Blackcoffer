# Data Extraction and Text Analysis

This repository contains Python scripts for extracting textual data from provided URLs (`article_extraction.py`) and performing text analysis (`text_analysis.py`). The scripts are designed to fulfill the requirements outlined in the "Data Extraction and NLP Test Assignment" provided by Blackcoffer.

## 1. Data Extraction (`article_extraction.py`)

### Instructions

1. Install the required dependencies using the following command:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the data extraction script:
    ```bash
    python article_extraction.py
    ```
   This script extracts text from specified URLs and saves it in the `article_data` directory.

### Script Overview

- The script utilizes BeautifulSoup and requests for web scraping.
- Extracted text is saved in individual text files named with the URL_ID.

## 2. Text Analysis (`text_analysis.py`)

### Instructions

1. Ensure the data extraction step is completed.
2. Run the text analysis script:
    ```bash
    python text_analysis.py
    ```
   This script performs textual analysis on the extracted data and generates an output file (`output_file.xlsx`).

### Script Overview

- The script performs sentiment analysis, readability analysis, and calculates various text-related metrics.
- It uses NLTK for tokenization and syllable counting.

## Folder Structure

```plaintext
- article_data
- article_extraction.py
- Input
  - Input.xlsx
  - MasterDictionary
    - negative-words.txt
    - positive-words.txt
  - Objective.docx
  - Output Data Structure.xlsx
  - StopWords
    - StopWords_Auditor.txt
    - StopWords_Currencies.txt
    - StopWords_DatesandNumbers.txt
    - StopWords_Generic.txt
    - StopWords_GenericLong.txt
    - StopWords_Geographic.txt
    - StopWords_Names.txt
  - Text Analysis.docx
- output_file.xlsx
- requirements.txt
- text_analysis.py
- venv
```

## Additional Notes

- Ensure proper configuration in the `Input.xlsx` file.
- Review the content of the `Objective.docx` and `Text Analysis.docx` files for detailed explanations.
- Follow the specified timeline for completion.
- For any questions or concerns, please contact [rameezk2215@gmail.com].# Text_Analysis_Blackcoffer
