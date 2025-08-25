# Residency Program AI Education Search

This project scrapes residency program websites and finds any mention of education on AI, machine learning, or related technologies for residents.

## Features

- Scrapes residency program websites
- Searches for mentions of AI education using advanced matching
- Extracts context sentences for reporting
- Outputs structured results

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add residency program URLs:**
   - Put website URLs in `data/programs_list.txt`, one per line.

3. **Run scraper:**
   ```bash
   python src/scraper.py
   ```

4. **Search for AI education mentions:**
   ```bash
   python src/search_ai_education.py
   ```

5. **Review results:**  
   - See `data/results.json` for search findings.

## Project Structure

- `src/` — source code
- `data/` — URLs and results
- `tests/` — unit tests

## Requirements

See `requirements.txt`.
