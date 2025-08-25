import os
import re
import json
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

KEYWORDS = [
    "artificial intelligence",
    "AI education",
    "AI track",
    "machine learning",
    "AI curriculum",
    "AI training",
    "AI for residents",
    "A.I.",
    "ML",
    "deep learning",
    "ai",
    "ai residency",
    "ai module",
    "ai bootcamp",
    "ai seminar",
    "ai workshop",
    "ai certificate",
    "ai fellowship",
    "ai rotation",
    "ai course",
    "ai didactics",
    "ai lecture",
    "ai program",
    "ai competency",
    "ai skills",
    "ai integration",
    "ai exposure",
    "ai-focused",
    "ai-based",
    "data science",
    "computational medicine",
    "informatics",
    "clinical informatics",
    "ai innovation",
    "ai literacy",
]

REGEX_PATTERNS = [
    r"\bai\b",
    r"\ba\.i\.\b",
    r"\bml\b",
    r"\bartificial intelligence\b",
    r"\bmachine learning\b",
    r"\bdeep learning\b",
    r"\bai[-\s]?education\b",
    r"\bai[-\s]?track\b",
    r"\bai[-\s]?curriculum\b",
    r"\bai[-\s]?training\b",
    r"\bai[-\s]?course\b",
    r"\bclinical informatics\b",
    r"\bcomputational medicine\b",
    r"\bdata science\b",
]

FUZZY_THRESHOLD = 85

def extract_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)

def find_keyword_context(text, keyword):
    sentences = extract_sentences(text)
    keyword_lower = keyword.lower()
    return [s for s in sentences if keyword_lower in s.lower()]

def advanced_search_for_ai_mentions(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=' ').strip()

    found = []

    # Regex matching
    for pattern in REGEX_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            context = find_keyword_context(text, match)
            found.append({
                "type": "regex",
                "keyword": match,
                "context": context
            })

    # Substring matching
    for keyword in KEYWORDS:
        if keyword.lower() in text.lower():
            context = find_keyword_context(text, keyword)
            found.append({
                "type": "keyword",
                "keyword": keyword,
                "context": context
            })

    # Fuzzy matching
    for keyword in KEYWORDS:
        score = fuzz.partial_ratio(keyword.lower(), text.lower())
        if score >= FUZZY_THRESHOLD and not any(f['keyword'] == keyword for f in found):
            context = find_keyword_context(text, keyword)
            found.append({
                "type": "fuzzy",
                "keyword": keyword,
                "score": score,
                "context": context
            })

    return found

def search_all_scraped_data(scraped_dir="data/scraped"):
    findings = []
    for fname in os.listdir(scraped_dir):
        if fname.endswith(".html"):
            file_path = os.path.join(scraped_dir, fname)
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            mentions = advanced_search_for_ai_mentions(html_content)
            if mentions:
                findings.append({
                    "file": fname,
                    "mentions": mentions,
                })
    return findings

def save_results(results, output_path="data/results.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

def main():
    results = search_all_scraped_data()
    save_results(results)
    print(f"Found AI education mentions in {len(results)} programs. See data/results.json.")

if __name__ == "__main__":
    main()
