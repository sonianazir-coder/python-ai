"""Lesson 1.4: Build an AI prompt from user input."""

# These details help personalize the prompt for the user's business.
name = input("Your name: ")
business = input("Business type: ")
problem = input("Biggest problem: ")

# A specific problem helps the AI suggest more relevant solutions.
prompt = f"Suggest 3 AI solutions for a {business} that struggles with {problem}."

print(f"\nWelcome, {name}!")
print("--- Your AI Prompt ---")
print(prompt)