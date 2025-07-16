# Offers SDK

A Python SDK for interacting with the Offers API. This package provides an easy-to-use async client for managing products and offers.

## Features

- **Async/await support** - 
- **Type safety** - Full type hints and models with Pydantic
- **HTTP client** - Uses httpx for HTTP requests
- **Authentication** - Handles JWT token refresh automatically
- **Product management** - Register and manage products
- **Offers retrieval** - Get offers for products

## Installation

The package is available on [TestPyPI](https://test.pypi.org/project/offers-sdk/).

### Using pip

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ offers-sdk
```

### Using Poetry

```bash
# Install from TestPyPI
poetry add --index-url https://test.pypi.org/simple/ offers-sdk

# Or install from local source
poetry install
```

## Quick Start

```python
import asyncio
from offers_sdk import OffersClient

async def main():
    # Initialize the client with your refresh token
    client = OffersClient(refresh_token="your-refresh-token-here")
    
    # Register a new product
    product = await client.register_product(
        name="My Product",
        description="A great product description"
    )
    print(f"Registered product: {product.name} (ID: {product.id})")
    
    # Get offers for the product
    offers = await client.get_offers(str(product.id))
    print(f"Found {len(offers)} offers")
    
    for offer in offers:
        print(f"- ${offer.price} (Stock: {offer.items_in_stock})")

if __name__ == "__main__":
    asyncio.run(main())
```

### Prerequisites

- Python 3.12+
- Poetry for dependency management

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/micholenko/dxheroes-task.git
cd dxheroes-task

# Install dependencies with Poetry
poetry install

# Run commands in the virtual environment
poetry run python your_script.py
```

### Running Tests

The project uses pytest for testing with support for async tests:

```bash
# Run all tests
poetry run pytest
```