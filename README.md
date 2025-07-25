# Challenge 1B: Multi-Collection PDF Analysis - Adobe DeepDoc

## 👤 Author
*Shrimant Sharma, Manya Sewkani, Abel Sangeeth*  
GitHub Repo: [Adobe-Deepdoc-round1b-](https://github.com/Shri32/Adobe-Deepdoc-round1b-)


##  Overview

This solution performs advanced PDF analysis over multiple document collections. It processes scanned and digital documents, filters out noise and garbage, and extracts the **most relevant sections based on a given persona and task**. The system is built to **rank sections**, extract clean text, and present it in a structured JSON output, similar to what Adobe expects.



##  Project Structure

adobe-round1b/
├── input/ # All input PDFs go here
├── output/ # Outputs clean JSON summary here
├── app/
│ └── summarizer.py # Main processing script
├── requirements.txt # Python dependencies
├── venv/ # Python virtual environment (local)
└── README.md # You're reading it!


##  Key Features

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


## 🧠 How It Works

1. *Input*: User specifies a persona and job/task (e.g., "Bank assistant preparing a financial report").
2. *Processing*:
   - All PDFs in `/input` are read
   - Text is extracted using PyMuPDF; OCR is used as fallback
   - Text is split into sections by titles
   - Sections are matched to relevant keywords based on detected job type
   - Summaries and insights are generated
3. *Output*:
   - `round1b_output.json` is created in `/output` folder
   - Contains extracted sections and analysis with ranks and reasons

##  Sample Output Structure

###  Input JSON (like `challenge1b_input.json`):
```json
{
  "challenge_info": {
    "challenge_id": "round_1b_financial",
    "test_case_name": "bank_report"
  },
  "documents": [{"filename": "annual1.pdf", "title": "Annual Report"}],
  "persona": {"role": "Bank Assistant"},
  "job_to_be_done": {"task": "Prepare a financial annual report having income, sales etc"}
}
##Output JSON (round1b_output.json):


{
  "metadata": {
    "input_documents": ["annual1.pdf"],
    "persona": "Bank Assistant",
    "job_to_be_done": "Prepare a financial annual report having income, sales etc"
  },
  "extracted_sections": [
    {
      "document": "annual1.pdf",
      "section_title": "3. Revenue and Sales",
      "importance_rank": 1,
      "page_number": 5
    }
  ],
  "subsection_analysis": [
    {
      "document": "annual1.pdf",

      "section_title": "3. Revenue and Sales",
      "refined_text": "In 2023, revenue increased by 12% to reach 1.2 billion USD...",
      "page_number": 5,
      "reason": "Matched: revenue, sales, income",
      "summary_insight": "Revenue increased 12% YoY, driven by strong sales in APAC.",
      "relevance_score": 0.67
    }
  ]
}
Supported Job Types
Financial Analysis → revenue, growth, market, R&D

Literature Review → methods, datasets, benchmarks

Exam Summaries → key concepts, mechanisms, examples

Custom User Tasks → Any custom job entered by the user will also be handled using fallback pattern-based extraction and generic summarization logic.

##Setup Instructions

# Clone the repo
git clone https://github.com/Shri32/Adobe-Deepdoc-round1b-.git
cd Adobe-Deepdoc-round1b-

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the processor
python app/summarizer.py
Highlights & Engineering Achievements
OCR fallback for even the weakest scanned PDFs

Garbage filtering that skips irrelevant control-text pages

Relevance Scoring to quantify how well a section matches the persona’s task

# Smart handling of both image-based and text-based PDFs

# Fast, lightweight, and modular design

# Future Improvements
Add UI/CLI flags for persona + job input

Add support for multilingual PDF processing

Create individual collection folders (if required)


##Made by Shrimant Sharma, Manya Sewkani and Abel Sangeeth
