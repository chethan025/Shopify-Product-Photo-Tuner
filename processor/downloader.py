import os
import requests
from PIL import Image
from io import BytesIO

def ensure_product_dirs(handle):
    os.makedirs(f"images/downloaded/{handle}", exist_ok=True)
    os.makedirs(f"images/no_bg/{handle}", exist_ok=True)

def download_image(url, handle, image_id):
    ensure_product_dirs(handle)

    response = requests.get(url)
    image = Image.open(BytesIO(response.content)).convert("RGBA")

    path = f"images/downloaded/{handle}/{handle}_{image_id}.png"
    image.save(path)

    return image