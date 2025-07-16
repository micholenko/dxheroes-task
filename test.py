import asyncio
from offers_sdk import OffersClient

async def main():
    # Initialize the client with your refresh token
    client = OffersClient(refresh_token="d4803215-2340-4dc1-aaf1-4183d58ec66c")
    
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