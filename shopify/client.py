import requests
import time
from config import SHOP, TOKEN, API_VERSION, REQUEST_DELAY

HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}
def request(method, endpoint, payload=None):
    response = request_raw(method, endpoint, payload)
    return response.json()


def request_raw(method, endpoint, payload=None):
    url = f"https://{SHOP}/admin/api/{API_VERSION}/{endpoint}"
    response = requests.request(method, url, headers=HEADERS, json=payload)
    time.sleep(REQUEST_DELAY)

    if not response.ok:
        raise Exception(response.text)

    return response