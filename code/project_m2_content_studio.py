"""AI Content Studio creates bakery menus, social posts, and customer replies."""

import time
from langchain.chat_models import init_chat_model


# Store settings in one place so the model and memory can be changed easily.
config = {
    "model": "llama3.2:latest",
    "max_messages": 8,
}

# Keep real business information here to reduce incorrect AI answers.
facts = {
    "name": "Sweet Crumbs Bakery",
    "city": "Lahore",
    "hours": "9 AM to 10 PM",
    "delivery": "Available in Lahore",
    "delivery_fee": 200,
    "free_delivery_minimum": 3000,
    "speciality": "Fresh cakes, cupcakes, and brownies",
    "prices": {
        "chocolate cake": 1500,
        "cupcake": 250,
        "brownie": 300,
        "mango tart": 0,
    },
}

# Give each tone a clear description so the owner can choose a writing style.
tones = {
    "fun": "playful, energetic, and friendly",
    "premium": "elegant, calm, and focused on quality",
    "urgent": "exciting, short, and encouraging customers to order soon",
}

# Use a low temperature for accurate customer replies.
precise = init_chat_model(
    config["model"],
    model_provider="ollama",
    temperature=0.2,
)

# Use a higher temperature for varied marketing content.
creative = init_chat_model(
    config["model"],
    model_provider="ollama",
    temperature=0.8,
)

system_message = {
    "role": "system",
    "content": (
        f"You are the customer assistant for {facts['name']} in {facts['city']}. "
        f"Opening hours: {facts['hours']}. "
        f"Delivery: {facts['delivery']}. "
        f"Delivery fee: {facts['delivery_fee']} PKR. "
        f"Free delivery on orders from {facts['free_delivery_minimum']} PKR. "
        f"Speciality: {facts['speciality']}. "
        f"Menu prices: {facts['prices']}. "
        "Only use the business facts provided in this message. "
        "Do not invent prices, products, opening hours, or policies. "
        "If you do not know an answer from these facts or the conversation, "
        "clearly say that you do not know."
    ),
}

messages = [system_message]

chat_answers = 0
menu_descriptions = 0
posts = 0
price_answers = 0
total_tokens = 0
total_seconds = 0.0

print("=" * 50)
print(f"       {facts['name']} AI Content Studio")
print("=" * 50)
print("Commands: /menu, /post fun|premium|urgent, /price <item>, /reset, bye")

while True:
    question = input("\nYou: ").strip()

    # Ignore empty input so the AI does not receive a blank message.
    if not question:
        print("Studio: Please enter a question or command.")
        continue

    command = question.lower()

    if command == "bye":
        print("Studio: Goodbye!")
        break

    elif command == "/reset":
        # Keep the system message because it contains the business rules.
        messages = [system_message]
        print("Studio: Conversation memory has been reset.")

    elif command == "/menu":
        menu_results = []

        for item, price in facts["prices"].items():
            if price == 0:
                print(f"Studio: Skipping {item} (coming soon).")
                continue

            # Creative writing makes product descriptions more attractive.
            menu_prompt = (
                f"Write one short sentence describing {item} for "
                f"{facts['name']} in {facts['city']}. "
                "Use appealing but truthful wording. Return only one sentence."
            )

            start_time = time.perf_counter()
            response = creative.invoke(menu_prompt)
            elapsed = time.perf_counter() - start_time

            description = response.text
            usage = response.usage_metadata or {}
            tokens = usage.get("input_tokens", 0) + usage.get("output_tokens", 0)

            total_tokens += tokens
            total_seconds += elapsed
            menu_descriptions += 1

            menu_results.append({
                "item": item,
                "price": price,
                "text": description,
            })

        print("-" * 50)

        for number, result in enumerate(menu_results, start=1):
            print(f"{number}. {result['item'].title()} ({result['price']:,} PKR)")
            print(f"   {result['text']}")

        print("-" * 50)

    elif command.startswith("/post"):
        parts = question.split(maxsplit=1)
        requested_tone = parts[1].lower() if len(parts) > 1 else ""

        # A default tone prevents an unknown tone from crashing the program.
        tone_description = tones.get(
            requested_tone,
            "friendly, clear, and professional",
        )

        post_prompt = (
            f"Write a short social media post for {facts['name']} in "
            f"{facts['city']}. Tone: {tone_description}. "
            f"Opening hours: {facts['hours']}. "
            f"Speciality: {facts['speciality']}. "
            f"Use only these facts and do not invent offers or prices."
        )

        print(f"Studio ({tone_description}):")
        start_time = time.perf_counter()
        post_tokens = 0

        for chunk in creative.stream(post_prompt):
            print(chunk.text, end="", flush=True)

            # Streaming responses may provide usage data in the final chunk.
            usage = chunk.usage_metadata or {}
            post_tokens = max(
                post_tokens,
                usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
            )

        elapsed = time.perf_counter() - start_time
        print()

        total_tokens += post_tokens
        total_seconds += elapsed
        posts += 1

    elif command.startswith("/price"):
        parts = question.split(maxsplit=1)
        requested_item = parts[1].strip().lower() if len(parts) > 1 else ""

        # Price questions use the real dictionary instead of spending AI tokens.
        if requested_item in facts["prices"]:
            price = facts["prices"][requested_item]

            if price == 0:
                print(f"Studio: {requested_item.title()} is coming soon.")
            else:
                print(f"Studio: {requested_item.title()} costs {price:,} PKR.")
        elif requested_item:
            print(f"Studio: {requested_item.title()} is not on our menu.")
        else:
            print("Studio: Please enter an item, for example /price cupcake.")

        price_answers += 1

    else:
        messages.append({"role": "user", "content": question})

        # Keep the system rules and only the most recent conversation messages.
        messages = [messages[0]] + messages[1:][-config["max_messages"]:]

        start_time = time.perf_counter()
        response = precise.invoke(messages)
        elapsed = time.perf_counter() - start_time

        answer = response.text
        usage = response.usage_metadata or {}
        tokens = usage.get("input_tokens", 0) + usage.get("output_tokens", 0)

        total_tokens += tokens
        total_seconds += elapsed
        chat_answers += 1

        messages.append({"role": "assistant", "content": answer})

        print(f"Studio: {answer}")
        print(
            f"(memory: {len(messages) - 1} messages, "
            f"{tokens:,} tokens sent/received)"
        )

print("=" * 50)
print("Session Report")
print("=" * 50)
print(f"Chat answers: {chat_answers}")
print(f"Menu descriptions: {menu_descriptions}")
print(f"Posts: {posts}")
print(f"Price answers: {price_answers}")
print(f"AI usage: {total_tokens:,} tokens in {total_seconds:.1f} seconds")
print("=" * 50)