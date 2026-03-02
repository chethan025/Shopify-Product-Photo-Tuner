import os

from shopify.selector import select_collection
from shopify.collections import get_products_by_collection
from shopify.images import (
    upload_product_image,
    delete_product_image,
    assign_variant_image
)
from processor.downloader import download_image
from processor.bg_remove import remove_background


def main():
    # 1. Select collection
    collection = select_collection()

    print(f"\nFetching products from '{collection['title']}'...\n")

    products = get_products_by_collection(collection["id"])

    print(f"\nSelected: {collection['title']}")
    print(f"Total products found: {len(products)}")

    if len(products) == 0:
        print("No products found in this collection. Exiting.")
        return

    confirm = input("\nProceed? (y/n): ").strip().lower()

    if confirm != "y":
        print("Aborted.")
        return

    print("\nStarting full product processing...\n")

    for product in products[:20]:
        product_id = product["id"]
        handle = product["handle"]

        print(f"\nProcessing product: {handle}")

        for image in product["images"]:
            image_id = image["id"]
            image_url = image["src"]
            variant_ids = image.get("variant_ids", [])

            print(f"  → Processing image {image_id}")

            try:
                # 1. Download
                img = download_image(image_url, handle, image_id)

                # 2. Remove Background
                processed = remove_background(img)

                # 3. Upload new image
                new_image = upload_product_image(
                    product_id,
                    processed,
                    f"{handle}_{image_id}.png"
                )

                new_image_id = new_image["id"]

                print(f"    Uploaded new image ID: {new_image_id}")

                # 4. Reassign variants (if any)
                for variant_id in variant_ids:
                    assign_variant_image(variant_id, new_image_id)
                    print(f"    Variant {variant_id} reassigned")

                # 5. Delete old image
                delete_product_image(product_id, image_id)
                print(f"    Deleted old image {image_id}")

            except Exception as e:
                print(f"    Failed on image {image_id}: {e}")

    print("\nAll products processed.\n")

    # -------------------------------------------------
    # 4. Future: Full product loop goes here
    # -------------------------------------------------
    # for product in products:
    #     process_product(product)


if __name__ == "__main__":
    main()