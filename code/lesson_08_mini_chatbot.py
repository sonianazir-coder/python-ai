"""Lesson 1.8: Rule-based chatbot for Sweet Crumbs Bakery."""

bot_name = "Sweet Crumbs Bot"

print(f"{bot_name}: Hi! Ask about timings, prices, location or orders. Type 'bye' to exit.")

# Ask for the user's name once before the conversation starts.
user_name = input(f"{bot_name}: What is your name? ").strip().title()

if user_name == "":
    user_name = "Friend"

# Why: These counters help us summarize the conversation.
message_count = 0
unanswered_count = 0
complaint_count = 0

while True:
    message = input(f"{user_name}: ").strip().lower()

    # Exit commands are checked before other rules.
    if message == "bye" or message == "exit":
        print(f"{bot_name}: Take care, {user_name}!")
        break

    message_count += 1

    if message == "":
        print(f"{bot_name}: Please type a question.")

    # Why: Complaints must be handled before general questions.
    elif (
        "complaint" in message
        or "refund" in message
        or "late" in message
        or "human" in message
        or "agent" in message
    ):
        complaint_count += 1
        print(f"{bot_name}: Sorry about that. Connecting you to a human...")

    elif "hour" in message or "timing" in message or "open" in message:
        print(f"{bot_name}: We are open from 9 AM to 10 PM every day.")

    elif "price" in message or "cost" in message or "how much" in message or "fee" in message:
        print(f"{bot_name}: Cakes start at 1,500 PKR. Cupcakes are 250 PKR each.")

    elif "where" in message or "location" in message or "address" in message:
        print(f"{bot_name}: Our example address is Main Boulevard, Lahore.")

    elif "order" in message or "delivery" in message:
        print(f"{bot_name}: Please contact the bakery directly to place an order.")

    elif message in ("hi", "hello") or message.startswith("salam"):
        print(f"{bot_name}: Hello, {user_name}! How can I help you?")

    else:
        unanswered_count += 1

        # Why: This prompt demonstrates how Module 2 can use an AI model.
        ai_prompt = (
            f"You are the friendly assistant of Sweet Crumbs Bakery. "
            f"Answer in 2 lines: {message}"
        )

        print(f"{bot_name}: I am not sure yet. An AI could answer using this prompt:")
        print(f"AI prompt: {ai_prompt}")

print("=" * 40)
print(f"Chat summary: {message_count} messages, {unanswered_count} unanswered.")
print(f"Complaints received: {complaint_count}")
