# Adobe DeepDoc - Challenge 1B: Multi-Collection PDF Analysis

## Author
**Shrimant Sharma, Manya Sewkani, Abel Sangeeth**

GitHub Repo: [Adobe-Deepdoc-round1b-](https://github.com/Shri32/Adobe-Deepdoc-round1b-)

This repository contains the solution for *Round 1B* of the Adobe India Hackathon 2025.  
It showcases a robust PDF analysis pipeline that processes *multiple document collections* and extracts *relevant content* based on persona and job context.

## Project Structure

adobe-round1b/
├── Collection1/ # Research Papers (Exam context)
│ ├── PDFs/ # RP1, RP2...
│ ├── challenge1b_input.json # Input configuration
│ └── challenge1b_output.json # Extracted output
├── Collection2/ # Chemistry Exam Material
│ ├── PDFs/ # CHEM1, CHEM2...
│ ├── challenge1b_input.json
│ └── challenge1b_output.json
├── Collection3/ # Financial Annual Reports
│ ├── PDFs/ # ANNUAL1, ANNUAL2...
│ ├── challenge1b_input.json
│ └── challenge1b_output.json
├── app/
│ └── summarizer.py # Main processing logic
├── requirements.txt
└── README.mdt

## Key Features

- *Persona-based filtering* using domain-specific keywords
- *Relevance Scoring* for intelligent content ranking
- *Fallback to OCR* (Tesseract) if PDFs are image-based or weakly extractable
- *Smart Junk Filters*:
  - Skips pages with control characters
  - Skips low-alphabetic or empty content
  - Ignores duplicate pages
- *Dynamic Section Detection*:
  - Detects section titles using patterns (uppercase, numbering, etc.)
  - Accepts even fallback sections if useful
- *Clean & Concise Summary* generation with insights
- *Well-structured JSON Output* for downstream applications

##  How to Run??

### Set up your environment


git clone https://github.com/Shri32/Adobe-Deepdoc-round1b-.git
cd Adobe-Deepdoc-round1b-
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 1. Run the processor

python3 app/summarizer.py

### 2. Output

Each collection will generate:

challenge1b_output.json under its folder

Logs showing skipped/cleaned pages, matched titles, and scores

##Supported Job Types

The system supports intelligent filtering and matching based on the following categories:

Literature Review

Financial Reports

Exam Study Material

Any Custom Job Provided by User – handled via fallback matching & title heuristics

# Sample Outputs

Collection      	Output Link

Research (Collection1)	[Sample Output - Collection 1](https://github.com/Shri32/Adobe-Deepdoc-round1b-/blob/main/Collection1/challenge1b_output.json)
Chemistry (Collection2)	[Collection 2 Output](https://github.com/Shri32/Adobe-Deepdoc-round1b-/blob/main/Collection2/challenge1b_output.json)
Finance (Collection3)	  [Collection 3 Output](https://github.com/Shri32/Adobe-Deepdoc-round1b-/blob/main/Collection3/challenge1b_output.json)


###Example Command to Process One Collection

Edit app/summarizer.py like:

input_docs = ["rp1.pdf.pdf", "rp2.pdf.pdf"]
job = "Prepare an exam report"
persona = "Exam evaluator"
Then run:

python3 app/summarizer.py
Output will be saved to:

output/round1b_output.json
Move and rename as needed:

mv output/round1b_output.json Collection1/challenge1b_output.json

###Highlights & Engineering Achievements

OCR fallback for even the weakest scanned PDFs

Garbage filtering that skips irrelevant control-text pages

Relevance Scoring to quantify how well a section matches the persona’s task

Smart handling of both image-based and text-based PDFs

Fast, lightweight, and modular design


### Final Notes

All PDF extraction works offline.

All models and code are CPU-compatible (no >1GB requirements).

No internet is required during execution.




