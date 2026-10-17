"""Lesson 1.7: Choose an AI model using conditions and estimate cost."""

# Ask for the task type and clean the text to handle different capital letters.
task = input("Task (code / private / chat): ").strip().lower()

# Convert the token input to an integer so Python can compare it with numbers.
tokens = int(input("Estimated tokens: "))

# Local models keep private data on the laptop, so their example cost is zero.
if task == "private":
    model = "gemma3:1b (local, Ollama)"
    price_per_1k_tokens = 0.0
elif task == "code":
    model = "Claude (cloud)"
    price_per_1k_tokens = 2.0
elif task == "chat":
    model = "Small cloud model"
    price_per_1k_tokens = 0.5
else:
    model = "Unknown task"
    price_per_1k_tokens = 0.0

# Long requests may need to be shortened before sending them to a model.
if tokens > 4000:
    warning = "Long request: consider shortening it."
else:
    warning = "Length is fine."

# Calculate an example cost using the selected model's practice price.
cost = tokens / 1000 * price_per_1k_tokens

print("\n" + "=" * 40)
print("SMART MODEL ROUTER")
print("=" * 40)
print(f"Task: {task}")
print(f"Chosen model: {model}")
print(warning)
print(f"Estimated cost: {cost:.2f} PKR")
print("=" * 40)