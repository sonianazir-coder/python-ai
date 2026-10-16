"""Lesson 1.5: Create an AI Model Profile Card."""

# Store the model's basic information in variables.
model_name = "gemma3:1b"
context_window = 32768
price_per_1k_tokens = 0.5
runs_locally = True

# Clear variable names make the model configuration easier to understand.
print("--- AI Model Profile Card ---")

print(f"Model Name: {model_name} | Type: {type(model_name)}")
print(f"Context Window: {context_window} | Type: {type(context_window)}")
print(f"Price per 1K Tokens: {price_per_1k_tokens} | Type: {type(price_per_1k_tokens)}")
print(f"Runs Locally: {runs_locally} | Type: {type(runs_locally)}")

# input() returns text, so int() converts the token count into a number.
tokens_used = int(input("\nHow many tokens does your chat use? "))

# This is an example price for practice, not the real price of Gemma.
cost = (tokens_used / 1000) * price_per_1k_tokens

print(f"Estimated Cost: {round(cost, 2)} PKR")

# Ask for daily chats to estimate the cost over 30 days.
chats_per_day = int(input("\nHow many chats do you use per day? "))

monthly_tokens = tokens_used * chats_per_day * 30
monthly_cost = (monthly_tokens / 1000) * price_per_1k_tokens

print(f"Estimated Monthly Cost: {round(monthly_cost, 2)} PKR")0