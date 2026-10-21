"""Lesson 1.7: Choose an AI model based on the task."""

# Ask the user for the task and clean the input.
task_type = input("Task (code / private / chat): ").strip().lower()
estimated_tokens = int(input("Estimated tokens: "))

# Why: Different tasks may need different models.
if task_type == "code":
    model_name = "claude (cloud, strong at code)"
    price = 0.80

elif task_type == "private":
    model_name = "llama3.2 (local, Ollama)"
    price = 0.0

else:
    model_name = "cheap chat model (cloud)"
    price = 0.20

# Why: Long requests may need shortening before sending.
if estimated_tokens > 4000:
    print("Warning: long request, consider shortening it.")
else:
    print("Length is fine.")

estimated_cost = (estimated_tokens / 1000) * price

print(f"Chosen model: {model_name}")
print(f"Estimated cost: {estimated_cost:.2f} PKR")

# Stretch: Check whether a free user needs to upgrade.
paid_user = input("Is this a paid user? (yes/no): ").strip().lower()

if paid_user == "no" and estimated_tokens > 2000:
    print("Upgrade to send long requests.")