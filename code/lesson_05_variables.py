"""Lesson 1.5: AI Model Profile Card with cost estimation."""

# Store the model details using four different Python data types.
model_name = "llama3.2"
context_window_tokens = 128000
price_per_1k_tokens_pkr = 0.50
runs_locally = True

# Why: The profile helps a user compare the model's basic information.
print("--- AI Model Profile Card ---")
print(f"Model: {model_name} {type(model_name)}")
print(f"Context window: {context_window_tokens} tokens {type(context_window_tokens)}")
print(f"Price per 1K tokens: {price_per_1k_tokens_pkr} PKR {type(price_per_1k_tokens_pkr)}")
print(f"Runs locally: {runs_locally} {type(runs_locally)}")

# Why: int() converts the entered token count into a whole number.
tokens_per_chat = int(input("Tokens per chat: "))

estimated_cost = (tokens_per_chat / 1000) * price_per_1k_tokens_pkr
print(f"Estimated cost: {round(estimated_cost, 2)} PKR")

# Stretch: Estimate the monthly cost for 30 days.
chats_per_day = int(input("Chats per day: "))
monthly_cost = estimated_cost * chats_per_day * 30

print(f"Estimated monthly cost: {round(monthly_cost, 2)} PKR")
