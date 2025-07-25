# app/pattern_engine.py

from app.config import IMPORTANT_SECTIONS, RECOMMENDED_SECTIONS

def rank_section(title):
    """
    Rank section importance: 1 = High (important), 2 = Medium (recommended), 3 = Low (others)
    """
    title_lower = title.lower()
    for keyword in IMPORTANT_SECTIONS:
        if keyword.lower() in title_lower:
            return 1
    for keyword in RECOMMENDED_SECTIONS:
        if keyword.lower() in title_lower:
            return 2
    return 3
def detect_patterns(text, section_title):
    """
    Trims and refines extracted section text.
    """
    lines = text.strip().split('\n')
    cleaned = []

    for line in lines:
        line = line.strip()
        if len(line) > 5 and not line.lower().startswith(("introduction", "background")):
            cleaned.append(line)
        if len(" ".join(cleaned)) > 700:  # or use SUMMARY_CHAR_LIMIT
            break

    return " ".join(cleaned)
