from shopify.client import request, request_raw

def get_collections():
    custom = request("GET", "custom_collections.json")["custom_collections"]
    smart = request("GET", "smart_collections.json")["smart_collections"]

    # Add a type field so we know what we're dealing with
    for c in custom:
        c["collection_type"] = "manual"

    for s in smart:
        s["collection_type"] = "smart"

    return custom + smart

def get_products_by_collection(collection_id):
    products = []
    endpoint = f"products.json?collection_id={collection_id}&limit=5"

    while endpoint:
        print("Requesting:", endpoint)

        response = request_raw("GET", endpoint)
        data = response.json()

        batch = data.get("products", [])
        print("Products returned:", len(batch))

        products.extend(batch)

        link = response.headers.get("Link")

        next_endpoint = None

        if link:
            links = link.split(",")

            for l in links:
                if 'rel="next"' in l:
                    next_url = l.split(";")[0].strip().strip("<>").strip()
                    next_endpoint = next_url.split("/admin/api/")[1].split("/", 1)[1]
                    break

        endpoint = next_endpoint

    return products