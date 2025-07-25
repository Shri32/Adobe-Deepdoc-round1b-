import os
import json
import datetime
import re
import unicodedata
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

# CONFIGS
SUMMARY_CHAR_LIMIT = 400
INPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../input"))
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../output"))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "round1b_output.json")

# CATEGORY KEYWORDS FOR DIFFERENT JOBS
JOB_CATEGORY_KEYWORDS = {
    "literature": {
        "methodologies": ["method", "approach", "architecture", "technique"],
        "datasets": ["data", "dataset", "corpus", "benchmark", "evaluation"],
        "performance_benchmarks": ["result", "performance", "accuracy", "comparison", "metrics"]
    },
    "financial": {
        "revenue_trends": ["revenue", "income", "sales", "profit", "ebitda", "growth"],
        "rnd_investments": ["research", "r&d", "development", "innovation"],
        "market_positioning": ["market", "strategy", "position", "competition"]
    },
    "exam": {
        "key_concepts": ["concept", "definition", "principle", "structure", "atomic", "bond"],
        "mechanisms": ["reaction", "process", "oxidation", "reduction", "step", "conversion"],
        "examples": ["example", "illustration", "case", "application", "uses"]
    },
    "general": {
        "relevant_content": [
            "overview", "conclusion", "important", "summary", "highlight", "main idea",
            "objective", "findings", "key points", "introduction", "impact", "benefit", "challenges"
        ]
    },
}

def detect_job_type(job):
    job = job.lower()
    if "literature" in job:
        return "literature"
    elif "financial" in job or "revenue" in job or "bank" in job:
        return "financial"
    elif "exam" in job or "study" in job or "education" in job:
        return "exam"
    else:
        return "general"

def clean_text(text):
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def summarize(text):
    text = clean_text(text)
    sentences = [s for s in text.split(". ") if len(s.split()) > 5]
    joined = ". ".join(sentences)
    return joined[:SUMMARY_CHAR_LIMIT] + ("..." if len(joined) > SUMMARY_CHAR_LIMIT else "")

def extract_summary_insight(summary):
    for s in summary.split(". "):
        if len(s.split()) >= 6:
            return s.strip('.') + '.'
    return summary.strip('.') + '.'

def extract_text_per_page(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        try:
            text = page.get_text().strip()
            if len(text) < 30 or not re.search(r'[a-zA-Z]{4,}', text):
                raise ValueError("Weak text")
        except:
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)

        if sum(c in text for c in '\u0001\u0007\b\u000e\u0010\u0012') > 10:
            print(f"⚠️ Skipped page {i + 1} (control characters) in {pdf_path}")
            continue
        if len(re.findall(r'[a-zA-Z]', text)) < 20:
            print(f"⚠️ Skipped page {i + 1} (not enough alphabetic chars) in {pdf_path}")
            continue

        pages.append((i + 1, text))
    return pages

def process_documents():
    input_docs = ["annual1.pdf","annual2.pdf","annual3.pdf"]
    job = "Prepare a fin report"
    persona = "exam prep"

    job_type = detect_job_type(job)
    category_keywords = JOB_CATEGORY_KEYWORDS.get(job_type, {})

    output = {
        "metadata": {
            "input_documents": input_docs,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    seen = set()
    skipped = []

    for filename in input_docs:
        full_path = os.path.join(INPUT_DIR, filename)
        pages = extract_text_per_page(full_path)

        # Check document relevance
        full_text = " ".join([text for _, text in pages]).lower()
        keyword_hits = sum(full_text.count(kw) for cat in category_keywords.values() for kw in cat)

        if keyword_hits < 2:
            print(f"❌ Skipping {filename} — doesn't seem relevant to job: {job}")
            continue

        print(f"\n📄 Processing: {filename} (relevance hits: {keyword_hits})")

        for page_num, text in pages:
            if not text or len(text.strip()) < 40 or not any(c.isalpha() for c in text):
                continue

            if (filename, page_num) in seen:
                continue
            seen.add((filename, page_num))

            lines = text.splitlines()

            for i, line in enumerate(lines):
                title = unicodedata.normalize("NFKD", line.strip())
                if len(title.split()) > 12 or len(title) < 3:
                    continue
                if not re.match(r"^\d{1,2}(\.\d{1,2})?\.?", title) and title.upper() != title:
                    continue

                context = " ".join(lines[i:i + 8])
                summary = summarize(context)
                insight = extract_summary_insight(summary)

                # 🛑 Garbage filter: control chars, low alpha density, junk OCR
                garbage_score = sum(1 for c in title if ord(c) < 32)
                alphabet_ratio = sum(c.isalpha() for c in title) / max(len(title), 1)
                summary_alpha = sum(c.isalpha() for c in summary)

                if garbage_score > 3 or alphabet_ratio < 0.4 or summary_alpha < 25:
                    skipped.append(f"{filename} → {title} [garbage detected]")
                    continue

                matched = False
                for cat, keywords in category_keywords.items():
                    hits = [kw for kw in keywords if kw.lower() in title.lower() or kw.lower() in summary.lower()]
                    if hits:
                        output["extracted_sections"].append({
                            "document": filename,
                            "page_number": page_num,
                            "section_title": title,
                            "importance_rank": 1
                        })
                        output["subsection_analysis"].append({
                            "document": filename,
                            "section_title": title,
                            "refined_text": summary,
                            "page_number": page_num,
                            "reason": f"Matched: {', '.join(hits)}",
                            "summary_insight": insight,
                            "relevance_score": round(len(hits) / len(keywords), 2)
                        })
                        matched = True
                        break

                if not matched:
                    if re.match(r"^\d{1,2}(\.\d{1,2})?\.?", title):
                        output["extracted_sections"].append({
                            "document": filename,
                            "page_number": page_num,
                            "section_title": title,
                            "importance_rank": 2
                        })
                        output["subsection_analysis"].append({
                            "document": filename,
                            "section_title": title,
                            "refined_text": summary,
                            "page_number": page_num,
                            "reason": "Accepted by pattern (fallback)",
                            "summary_insight": insight,
                            "relevance_score": 0.5
                        })
                    else:
                        skipped.append(f"{filename} → {title} [no keyword or pattern match]")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)
        print(f"\n🎯 Summary JSON saved to: {OUTPUT_FILE}")

    if skipped:
        print("\n🟡 Skipped Sections:")
        for s in skipped:
            print(f"  - {s}")

if __name__ == "__main__":
    process_documents()


