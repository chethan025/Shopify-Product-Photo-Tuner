# Shopify Product Photo Tuner

A Python-based pipeline tailored for Shopify merchants.
It downloads product images, removes backgrounds using a BiRefNet model, and uploads or manages them via Shopify collections and APIs.

## Project Structure

- `processor/` - modules for downloading and background removal using BiRefNet. Clone the official repo into this folder for model code and weights.
- `shopify/` - client utilities for interacting with Shopify APIs.
- `tests/` - unit tests.
- `main.py` - entry point for orchestrating the pipeline.
- `config.py` - configuration settings.

## Setup

### Clone model repository

Before installing dependencies, clone the BiRefNet repository into `processor/`:

```bash
cd processor
git clone https://huggingface.co/ZhengPeng7/BiRefNet/ BiRefNet
cd ..
```

### Python environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file (or export variables directly) with the following format to configure Shopify API access and any other secrets:

```
SHOP=xxxxxx.myshopify.com
TOKEN=xxxxxxxxxxxxxxxxxxxxx
API_VERSION=2024-01
REQUEST_DELAY=0.6
```

The application reads these values via `config.py` using `python-dotenv`.

---

## How it works

This section breaks down the codebase and processing logic.

1. **Configuration (`config.py`)**
   - Loads environment variables for Shopify URL, access token, API version, and request pacing.
   - These values are used by the Shopify client module to authenticate and build request URLs.

2. **Shopify client utilities (`shopify/client.py`)**
   - Provides `request` and `request_raw` helpers that wrap `requests` and automatically wait between calls.
   - All HTTP interactions with the Shopify Admin API are centralized here.

3. **Collection and product handling (`shopify/collections.py`, `shopify/selector.py`)**
   - `get_collections()` fetches both manual and smart collections, tagging them with `collection_type`.
   - `get_products_by_collection()` paginates through `/products.json` for a given collection ID, honoring Shopify's `Link` header for next pages.
   - `select_collection()` presents a numbered list to the user and returns the chosen collection object.

4. **Image management (`shopify/images.py`)**
   - `upload_product_image()` converts a `PIL.Image` object into a base64-encoded PNG and posts it to Shopify.
   - `delete_product_image()` and `assign_variant_image()` wrap the corresponding API endpoints to clean up old images and reassign variants to the new ones.

5. **Downloader (`processor/downloader.py`)**
   - Ensures local directory structure under `images/downloaded/<handle>` and `images/no_bg/<handle>`.
   - Downloads images via `requests`, converts to RGBA, saves locally, and returns a PIL image instance.

6. **Background removal (`processor/bg_remove.py`)**
   - Loads a local BiRefNet model (cloned from Hugging Face) once at import time.
   - Exposes `remove_background()` which:
     * Resizes and normalizes the input image.
     * Runs inference to produce a segmentation mask.
     * Applies the mask to add an alpha channel to the original image.
     * Calls `process_to_portrait_with_crop()` to add padding, enforce a target aspect ratio(change the ratio as your preference), and crop around the object.
   - Runs on CUDA if available; automatically clears tensors after each run.

7. **Orchestration (`main.py`)**
   - Prompts the user to choose a collection and fetches all its products.
   - Iterates through each product and its images (currently limited to the first twenty products for safety).
   - For each image:
     * Downloads the original.
     * Removes the background.
     * Uploads the processed image back to Shopify.
     * Reassigns any product variants to use the new image.
     * Deletes the old image from Shopify.
   - Handles errors per-image and prints progress to the console.
   - Contains commented-out future logic for processing all products.

Together, these modules form a simple but extensible pipeline: download, process, and sync Shopify images with minimal manual effort.

## Usage

Run the main script or individual modules to perform the image processing tasks:

```bash
python main.py
```

## Contributing

Feel free to open issues or pull requests.

## License

Open Source

