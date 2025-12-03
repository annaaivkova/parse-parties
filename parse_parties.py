import json
from urllib.parse import urljoin, urlparse, urlunparse
import requests
from bs4 import BeautifulSoup
BASE_URL = "https://minjust.gov.ru"
TARGET_URL = "https://minjust.gov.ru/ru/pages/politicheskie-partii/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}

def clean_url(url: str) -> str | None:
    if not url:
        return None

    absolute = urljoin(BASE_URL, url)
    parsed = urlparse(absolute)
    return urlunparse(("https", parsed.netloc, parsed.path, "", "", ""))

def main():
    response = requests.get(TARGET_URL, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    parties = []
    party_items = soup.select("div.page-block-text ol li")
    for i in party_items:
        name_tag = i.select_one("a")
        if not name_tag:
            continue

        name = name_tag.get_text(strip=True)

        doc_link_tag = i.select_one("a[href]")
        doc_url = None
        if doc_link_tag and doc_link_tag.has_attr("href"):
            doc_url = clean_url(doc_link_tag["href"])

        parties.append({"name": name, "doc_url": doc_url})

    for p in parties:
        print(f"{p['name']} -> {p['doc_url']}")
    with open("parties.json", "w", encoding="utf-8") as f:
        json.dump(parties, f, ensure_ascii=False, indent=2)
if __name__ == "__main__":
    main()