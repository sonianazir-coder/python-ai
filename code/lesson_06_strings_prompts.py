"""Lesson 1.6: Clean and measure a user's question."""

# Ask for the user's name and question.
user_name = input("Your name: ")
messy_question = input("Your question: ")

# Why: strip() removes extra spaces before processing the text.
cleaned_name = user_name.strip().title()
cleaned_question = messy_question.strip().capitalize()

# Why: Character count helps estimate the size of a prompt.
character_count = len(cleaned_question)
estimated_tokens = round(character_count / 4)

mentions_python = "python" in cleaned_question.lower()

# Stretch: Replace the example bad word before building the prompt.
cleaned_question = cleaned_question.replace("stupid", "***")

print("=" * 40)
print(f"Cleaned question: {cleaned_question}")
print(f"Characters: {character_count}, about {estimated_tokens} tokens")
print(f"Mentions Python: {mentions_python}")
print("=" * 40)

# Slicing keeps the question within the required 150-character limit.
prompt = f"""You are a friendly Python tutor.
Greet {cleaned_name} by name and answer in 3 short lines.
Question: {cleaned_question[:150]}"""

print(prompt)

# Stretch: Calculate an example cost.
example_price_per_1k_tokens = 0.50
estimated_cost = (estimated_tokens / 1000) * example_price_per_1k_tokens

print(f"Estimated cost: PKR {estimated_cost:.2f}")
