# ~/shoonya/crawler.py

from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
import os
import time

def fetch_and_store(topic, count=3):
    web_dir = os.path.expanduser("~/shoonya/data/web")
    os.makedirs(web_dir, exist_ok=True)

    with DDGS() as ddgs:
        results = ddgs.text(topic, max_results=count)

        for i, r in enumerate(results):
            url = r['href']
            print(f"Fetching: {url}")
            try:
                html = requests.get(url, timeout=10).text
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.get_text()
                text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
                filename = os.path.join(web_dir, f"{topic.replace(' ', '_')}_{i+1}.txt")
                with open(filename, "w") as f:
                    f.write(text[:20000])  # Store first 20k chars
                print(f"Saved: {filename}")
                time.sleep(1)
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")

if __name__ == "__main__":
    topic = input("Enter topic to fetch: ")
    fetch_and_store(topic)

