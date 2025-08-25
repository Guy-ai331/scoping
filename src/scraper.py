import requests
from bs4 import BeautifulSoup
import os

def read_program_urls(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def save_content(url, content, output_dir="data/scraped"):
    os.makedirs(output_dir, exist_ok=True)
    filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
    with open(os.path.join(output_dir, f"{filename}.html"), "w", encoding="utf-8") as f:
        f.write(content)

def main():
    urls = read_program_urls("data/programs_list.txt")
    for url in urls:
        print(f"Scraping {url} ...")
        content = scrape_website(url)
        if content:
            save_content(url, content)

if __name__ == "__main__":
    main()
