import requests
from bs4 import BeautifulSoup

URLS = [
    "https://www.flipkart.com/about-us",
    "https://www.flipkart.com/helpcentre"
]

all_text = ""

for url in URLS:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    all_text += f"\n--- SOURCE: {url} ---\n{text}"

with open("data/flipkart_raw_text.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("✅ Flipkart website content extracted")