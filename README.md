# Xagon Background Pipeline

A Python-based pipeline tailored for Shopify merchants.
It downloads product images, removes backgrounds using a BiRefNet model, and uploads or manages them via Shopify collections and APIs.

## Project Structure

- `processor/` - modules for downloading and background removal using BiRefNet. Clone the official repo into this folder for model code and weights.
- `shopify/` - client utilities for interacting with Shopify APIs.
- `tests/` - unit tests.
- `main.py` - entry point for orchestrating the pipeline.
- `config.py` - configuration settings.

## Setup

Before installing dependencies, clone the BiRefNet repository into `processor/`:

```bash
cd processor
git clone https://huggingface.co/ZhengPeng7/BiRefNet/ BiRefNet
cd ..
```


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

Free for all




