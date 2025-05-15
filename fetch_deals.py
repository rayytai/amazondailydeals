# fetch_deals.py
import os, json, time
import requests
from bs4 import BeautifulSoup

AFFILIATE_TAG = os.getenv("PAAPI_PARTNER_TAG")  # e.g. yourtag-20
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_deals(max_items=100):
    url = "https://www.amazon.com/gp/goldbox?ref_=nav_cs_gb"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    deals = []
    # Amazon uses a lot of dynamic loading; here’s a CSS selector for the deal tiles
    items = soup.select("div.DealGridItem-module__dealItem")[:max_items]
    for it in items:
        a = it.select_one("a.a-link-normal")
        if not a or not a.get("href"):
            continue
        link = "https://www.amazon.com" + a["href"].split("?")[0] + f"?tag={AFFILIATE_TAG}"

        img = it.select_one("img")
        img_url = img["src"] if img and img.get("src") else ""

        title = it.select_one("span.DealContent-module__truncate_sWbxETx42ZPStTc9jwySW")
        title_text = title.get_text(strip=True) if title else "No title"

        price = it.select_one("span.a-price-whole")
        price_text = (price.get_text(strip=True) or "") + it.select_one("span.a-price-fraction").get_text(strip=True) \
                     if price and it.select_one("span.a-price-fraction") else "N/A"

        asin = link.split("/dp/")[-1].split("/")[0]

        deals.append({
            "asin": asin,
            "title": title_text,
            "price": price_text,
            "url": link,
            "img": img_url
        })
        time.sleep(0.2)  # be kind to Amazon

    return deals

if __name__ == "__main__":
    deals = scrape_deals(100)
    with open("deals.json", "w", encoding="utf-8") as f:
        json.dump(deals, f, indent=2)
    print(f"Wrote {len(deals)} deals to deals.json")
