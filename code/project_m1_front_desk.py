"""AI Front Desk for Sweet Crumbs Bakery.

Answers common questions, calculates order quotes, and prepares AI prompts.
"""

# Constants keep the business settings together in one place.
BOT_NAME = "Sweet Crumbs Desk"
BUSINESS_NAME = "Sweet Crumbs Bakery"
DELIVERY_FEE = 200
FREE_DELIVERY_LIMIT = 3000
CLOUD_PRICE_PER_1K_TOKENS = 0.10

print("=" * 50)
print(f"{BOT_NAME}: rules, quotes and AI-ready prompts")
print("=" * 50)
print("Ask anything, type /quote for a price, or bye to exit.")

# Why: Asking once lets the bot use the customer's name in every reply.
customer_name = input(f"{BOT_NAME}: What is your name? ").strip().title()

if customer_name == "":
    customer_name = "Customer"

# Session counters help the business understand customer activity.
message_count = 0
answered_count = 0
unanswered_count = 0
quote_count = 0
total_quoted_value = 0
total_ai_cost = 0.0
complaint_count = 0

while True:
    message = input(f"{customer_name}: ").strip().lower()

    if message == "bye":
        print(f"{BOT_NAME}: Goodbye, {customer_name}!")
        break

    message_count += 1

    if message == "":
        print(f"{BOT_NAME}: Please type a question.")
        continue

    # Why: Complaints are checked first so unhappy customers get priority.
    if (
        "refund" in message
        or "complaint" in message
        or "late" in message
        or "human" in message
        or "agent" in message
    ):
        complaint_count += 1
        answered_count += 1
        print(
            f"{BOT_NAME}: Sorry about that. "
            "A manager will call you within 1 hour."
        )

    elif message == "/quote":
        item_name = input(f"{BOT_NAME}: Which item? ").strip().lower()
        quantity_text = input(f"{BOT_NAME}: How many? ").strip()

        # Why: isdigit() checks quantity before int() to avoid invalid input.
        if not quantity_text.isdigit() or int(quantity_text) <= 0:
            print(f"{BOT_NAME}: Please enter a positive whole number.")
        else:
            quantity = int(quantity_text)

            if item_name == "cupcake":
                item_price = 250
            elif item_name == "brownie":
                item_price = 300
            elif item_name == "chocolate cake":
                item_price = 1500
            else:
                item_price = 0

            if item_price == 0:
                print(
                    f"{BOT_NAME}: Sorry, {item_name} "
                    "is not on our menu."
                )
            else:
                subtotal = item_price * quantity

                if quantity >= 10:
                    discount = subtotal * 0.10
                else:
                    discount = 0

                discounted_subtotal = subtotal - discount

                # Why: Delivery is decided after applying the discount.
                if discounted_subtotal >= FREE_DELIVERY_LIMIT:
                    delivery = 0
                else:
                    delivery = DELIVERY_FEE

                total = discounted_subtotal + delivery

                quote_count += 1
                answered_count += 1
                total_quoted_value += total

                print(
                    f"{BOT_NAME}: {quantity} x {item_name} = "
                    f"{subtotal:,} PKR"
                )
                print(
                    f"Discount: -{discount:,.0f} PKR | "
                    f"Delivery: {delivery:,} PKR"
                )
                print(f"Total: {total:,.0f} PKR")

    # Why: Specific rules are checked before the general AI fallback.
    elif "hour" in message or "timing" in message or "open" in message:
        answered_count += 1
        print(f"{BOT_NAME}: We are open 9 AM to 10 PM, every day.")

    elif "where" in message or "location" in message or "address" in message:
        answered_count += 1
        print(f"{BOT_NAME}: Our example address is Main Boulevard, Lahore.")

    elif "delivery" in message:
        answered_count += 1
        print(
            f"{BOT_NAME}: Delivery costs {DELIVERY_FEE} PKR. "
            f"Orders of {FREE_DELIVERY_LIMIT:,} PKR or more after "
            "discount receive free delivery."
        )

    elif "price" in message or "menu" in message or "cost" in message:
        answered_count += 1
        print(
            f"{BOT_NAME}: Cupcake: 250 PKR, Brownie: 300 PKR, "
            "Chocolate cake: 1,500 PKR."
        )

    elif message in ("hi", "hello") or message.startswith("salam"):
        answered_count += 1
        print(f"{BOT_NAME}: Hello, {customer_name}! How can I help you?")

    else:
        unanswered_count += 1

        clean_question = message.capitalize()[:150]
        estimated_tokens = round(len(clean_question) / 4)

        # Private details stay with a local model and have zero estimated cost.
        if (
            "phone" in message
            or "cnic" in message
            or "address" in message
        ):
            chosen_model = "llama3.2 (local, private)"
            estimated_cost = 0.0
        else:
            chosen_model = "small cloud model (cheap)"
            estimated_cost = (
                estimated_tokens / 1000
            ) * CLOUD_PRICE_PER_1K_TOKENS

        total_ai_cost += estimated_cost

        # The prompt is prepared for Module 2; this script does not send it.
        ai_prompt = f"""You are the assistant of {BUSINESS_NAME}.
Answer {customer_name} in 2 short lines.
Question: {clean_question}"""

        print(
            f"{BOT_NAME}: Good question! Routed to: {chosen_model} "
            f"(~{estimated_tokens} tokens)"
        )
        print(f"Estimated AI cost: {estimated_cost:.4f} PKR")
        print(f"Prompt:\n{ai_prompt}")

print("=" * 50)
print("Session report")
print(f"Messages: {message_count}")
print(f"Answered by rules: {answered_count}")
print(f"Unanswered: {unanswered_count}")
print(f"Quotes: {quote_count}")
print(f"Quoted value: {total_quoted_value:,} PKR")
print(f"Estimated AI cost: {total_ai_cost:.4f} PKR")
print(f"Complaints received: {complaint_count}")
print("=" * 50)