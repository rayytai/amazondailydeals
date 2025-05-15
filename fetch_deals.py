# fetch_deals.py
import os, json
from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models import SearchItemsRequest
from paapi5_python_sdk.client import Client

ACCESS_KEY  = os.getenv("PAAPI_ACCESS_KEY")
SECRET_KEY  = os.getenv("PAAPI_SECRET_KEY")
PARTNER_TAG = os.getenv("PAAPI_PARTNER_TAG")

client = Client(
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    partner_tag=PARTNER_TAG,
    host="webservices.amazon.com",
    region="us-east-1"
)
api = DefaultApi(client)

def get_deals():
    resp = api.search_items(
      SearchItemsRequest(
        partner_tag=PARTNER_TAG,
        partner_type="Associates",
        marketplace="www.amazon.com",
        browse_node_id="18549972011",
        item_count=100,
        resources=[
          "ItemInfo.Title",
          "Offers.Listings.Price",
          "Images.Primary.Large",
          "ItemInfo.ExternalIds.ASIN"
        ]
      )
    )
    items = []
    for it in resp.search_result.items:
        items.append({
            "asin": it.external_ids.asin.values[0],
            "title": it.item_info.title.display_value,
            "price": it.offers.listings[0].price.display_amount,
            "url": f"{it.detail_page_url}?tag={PARTNER_TAG}",
            "img": it.images.primary.large.url
        })
    return items

if __name__ == "__main__":
    deals = get_deals()
    with open("deals.json", "w") as f:
        json.dump(deals, f, indent=2)
    print(f"Wrote {len(deals)} deals to deals.json")
