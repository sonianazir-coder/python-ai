"""
Task 2.7: Order Extractor for Sweet Crumbs Bakery.

This program extracts customer orders from mixed English and
Roman Urdu messages, checks the extracted information, calculates
prices in Python, and saves valid orders to a JSON file.
"""

import json

from langchain.chat_models import init_chat_model


# Official bakery menu and prices.
PRICES = {
    "cupcake": 250,
    "chocolate cake": 1500,
    "brownie": 300,
    "cookies": 200,
    "vanilla cake": 1200,
}


# Different customer messages for testing.
MESSAGES = [
    "I want 2 cupcakes. My name is Sara, address is Johar Town.",

    "Salam! 2 cupcakes aur 1 chocolate cake chahiye. Ali, house 12 Gulberg",

    "1 pizza and 2 brownies, Bilal, Model Town",

    "Hi, do you deliver to Johar Town?",

    "Mujhe 3 brownies chahiye. Mera naam Ahmed hai, address DHA Lahore.",

]


# JSON schema tells the AI what structure to return.
ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "is_order": {
            "type": "boolean"
        },
        "customer_name": {
            "type": ["string", "null"]
        },
        "address": {
            "type": ["string", "null"]
        },
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string"
                    },
                    "quantity": {
                        "type": "integer"
                    }
                },
                "required": ["item", "quantity"]
            }
        }
    },
    "required": [
        "is_order",
        "customer_name",
        "address",
        "items"
    ]
}


# Why: Temperature 0 makes extraction more consistent and less creative.
extractor_model = init_chat_model(
    "llama3.2:latest",
    model_provider="ollama",
    temperature=0
).bind(format=ORDER_SCHEMA)


def extract_order(message: str) -> str:
    """Extract order details from a customer message as JSON."""

    prompt = f"""
    Extract order information from this customer message.

    Available menu:
    {json.dumps(PRICES, indent=2)}

    Rules:
    - Return only JSON matching the provided schema.
    - Identify whether the message is an actual order.
    - Extract the customer's name only if it appears in the message.
    - Extract the address only if it appears in the message.
    - Include ALL requested items, even if they are not on the menu.
    - Do not invent missing information.
    - If there is no order, set is_order to false and items to [].
    - Quantity must be a positive integer.

    Customer message:
    {message}
    """

    response = extractor_model.invoke(prompt)

    return response.content


def main() -> None:
    """Process customer messages and save checked orders."""

    orders = []
    checks = []
    total_value = 0

    for message in MESSAGES:

        print(f"\nMessage: {message}")

        try:
            raw_response = extract_order(message)

            # Why: JSON validation prevents incorrect AI output from
            # being used directly in business records.
            data = json.loads(raw_response)

        except json.JSONDecodeError:
            warning = "CHECK: AI returned invalid JSON."
            print(warning)
            checks.append(warning)
            continue

        # Read values safely with defaults.
        is_order = data.get("is_order", False)
        customer_name = data.get("customer_name")
        address = data.get("address")
        items = data.get("items", [])

        if not is_order:
            print("Not an order: needs a human reply.")
            continue

        order_total = 0
        checked_items = []

        for item_data in items:

            item_name = item_data.get("item", "").strip().lower()
            quantity = item_data.get("quantity", 0)

            if item_name not in PRICES:
                warning = f"CHECK: '{item_name}' is not on the menu."
                print(warning)
                checks.append(warning)
                continue

            if not isinstance(quantity, int) or quantity <= 0:
                warning = f"CHECK: Invalid quantity for '{item_name}'."
                print(warning)
                checks.append(warning)
                continue

            price = PRICES[item_name]
            line_total = price * quantity

            order_total += line_total

            checked_items.append({
                "item": item_name,
                "quantity": quantity,
                "unit_price": price,
                "line_total": line_total
            })

            print(
                f"  {quantity} x {item_name} = "
                f"{line_total} PKR"
            )

        # Why: A name invented by AI must not be saved as a real customer.
        if customer_name and customer_name.lower() not in message.lower():
            warning = (
                f"CHECK: Customer name '{customer_name}' "
                "was not found in the original message."
            )
            print(warning)
            checks.append(warning)
            customer_name = None

        if not customer_name:
            warning = "CHECK: Customer name is missing."
            print(warning)
            checks.append(warning)

        if checked_items:
            order = {
                "customer_name": customer_name,
                "address": address,
                "items": checked_items,
                "total": order_total
            }

            orders.append(order)
            total_value += order_total

            print(
                f"  Customer: {customer_name}, "
                f"Address: {address}"
            )
            print(f"  Total: {order_total} PKR")

    # Save all checked orders in JSON format.
    # Why: JSON keeps order information structured and reusable.
    with open("orders.json", "w", encoding="utf-8") as file:
        json.dump(
            orders,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\n" + "=" * 50)

    print(
        f"Orders found: {len(orders)} | "
        f"Total value: {total_value:,} PKR | "
        f"Checks: {len(checks)}"
    )

    print(f"Saved {len(orders)} orders to orders.json")


if __name__ == "__main__":
    main()