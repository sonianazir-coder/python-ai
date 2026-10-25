"""Generate product descriptions for a bakery and calculate usage."""

import time

from langchain.chat_models import init_chat_model


# These are the bakery products and their prices in PKR.
products = {
    "Chocolate Cake": 1500,
    "Cupcake": 250,
    "Brownie": 300,
    "Donut": 200,
    "Cookies": 180,
    "Old Stock": 0,
}

# Central configuration makes changing the model easier.
config = {
    "model": "llama3.2:latest",
    "temperature": 0.2,
}


def main():
    """Generate descriptions and print a numbered bakery menu."""

    # Create the model once so it can be reused for every product.
    llm = init_chat_model(
        config["model"],
        model_provider="ollama",
        temperature=config["temperature"],
    )

    results = []
    total_tokens = 0
    total_seconds = 0.0

    # .items() provides both the product name and its price.
    for name, price in products.items():

        # Skip products without a price to avoid unnecessary AI calls.
        if price == 0:
            print(f"Skipping {name} (no price)")
            continue

        prompt = (
            f"Write exactly one appealing sentence describing "
            f"{name} for Sweet Crumbs Bakery in Lahore. "
            f"Its price is {price} PKR. "
            "Do not invent ingredients or unsupported claims."
        )

        start_time = time.perf_counter()
        response = llm.invoke(prompt)
        elapsed = time.perf_counter() - start_time

        usage = response.usage_metadata or {}
        tokens = usage.get("total_tokens", 0)

        total_tokens += tokens
        total_seconds += elapsed

        # Store each result as a dictionary for printing later.
        results.append(
            {
                "item": name,
                "price": price,
                "text": response.text.strip(),
            }
        )

    print("=" * 50)

    # enumerate() numbers the products starting from 1.
    for number, product in enumerate(results, start=1):
        print(
            f"{number}. {product['item']} "
            f"({product['price']} PKR)"
        )
        print(f"   {product['text']}")

    print("=" * 50)
    print(
        f"{len(results)} descriptions, "
        f"{total_tokens} tokens, "
        f"{total_seconds:.1f} seconds"
    )


if __name__ == "__main__":
    main()
