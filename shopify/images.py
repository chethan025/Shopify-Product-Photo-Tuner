import base64
from io import BytesIO
from shopify.client import request

def upload_product_image(product_id, pil_image, filename):
    buffer = BytesIO()
    pil_image.save(buffer, format="PNG", optimize=True)

    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    payload = {
        "image": {
            "attachment": img_base64,
            "filename": filename
        }
    }

    data = request(
        "POST",
        f"products/{product_id}/images.json",
        payload
    )

    return data["image"]


def delete_product_image(product_id, image_id):
    request(
        "DELETE",
        f"products/{product_id}/images/{image_id}.json"
    )


def assign_variant_image(variant_id, image_id):
    payload = {
        "variant": {
            "id": variant_id,
            "image_id": image_id
        }
    }

    request(
        "PUT",
        f"variants/{variant_id}.json",
        payload
    )