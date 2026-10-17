"""Lesson 1.8: Rule-based chatbot for Sweet Crumbs Bakery."""


BOT = "Sweet Crumbs Bot"

print(f"{BOT}: Welcome! I can help you with bakery hours, prices, location and orders.")
print(f"{BOT}: Type 'bye' to end the chat.")

# Why: We ask the name once so the bot remembers it throughout the conversation.
name = input(f"{BOT}: What is your name? ").strip().title()

if name == "":
    name = "Friend"

print(f"{BOT}: Nice to meet you, {name}!")

# Why: These counters help us summarize the conversation at the end.
count = 0
unanswered = 0

while True:
    message = input(f"{name}: ").strip().lower()
    count += 1

    if message == "bye" or message == "exit":
        print(f"{BOT}: Goodbye, {name}! Thanks for visiting Sweet Crumbs Bakery.")
        break

    elif message == "":
        print(f"{BOT}: Please type a question.")

    # Why: Complaints come first so an unhappy customer gets priority.
    elif "refund" in message or "complaint" in message or "late" in message:
        print(f"{BOT}: Sorry about that, {name}. A manager will contact you.")

    elif "hour" in message or "open" in message or "time" in message:
        print(f"{BOT}: Our example opening hours are 9 AM to 10 PM every day.")

    elif "price" in message or "cost" in message or "how much" in message:
        print(f"{BOT}: Cakes start at 1,500 PKR. Cupcakes are 250 PKR each.")

    elif "where" in message or "location" in message or "address" in message:
        print(f"{BOT}: Our example address is Main Boulevard, Lahore.")

    elif "order" in message or "delivery" in message:
        print(f"{BOT}: Please contact the bakery directly to place an order.")

    # Exact matching prevents 'hi' from matching inside words like 'which'.
    elif message in ("hi", "hello") or message.startswith("salam"):
        print(f"{BOT}: Hello again, {name}! How can I help you?")

    else:
        unanswered += 1

        # Why: The prompt shows what we could send to an AI model in Module 2.
        prompt = (
            f"You are a friendly assistant for Sweet Crumbs Bakery. "
            f"Answer the customer in 2 short lines: {message}"
        )

        print(f"{BOT}: I don't know the answer yet.")
        print(f"{BOT}: An AI could answer using this prompt:")
        print(f"AI prompt: {prompt}")

print("=" * 40)
print(f"Chat summary: {count} messages, {unanswered} unanswered.")