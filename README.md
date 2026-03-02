# Xagon Background Pipeline

A Python-based pipeline tailored for Shopify merchants.
It downloads product images, removes backgrounds using a BiRefNet model, and uploads or manages them via Shopify collections and APIs.

## Project Structure

- `processor/` - modules for downloading and background removal using BiRefNet.
- `shopify/` - client utilities for interacting with Shopify APIs.
- `tests/` - unit tests.
- `main.py` - entry point for orchestrating the pipeline.
- `config.py` - configuration settings.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the main script or individual modules to perform the image processing tasks:

```bash
python main.py
```

## Contributing

Feel free to open issues or pull requests.

## License

Specify your license here.
