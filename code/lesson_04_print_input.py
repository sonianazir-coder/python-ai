"""Lesson 1.4: Build an AI prompt from user input."""

# Collect details from the user

name = input("Enter your name: ")
business = input("Enter your business type (e.g. bakery): ")
problem = input("What problem does your business face? ")

# Use an f-string to insert the user's details into the prompt

prompt = f"Suggest 3 AI solutions for a {business} that struggles with {problem}."

# Welcome the user and display the final prompt

print(f"\nWelcome, {name}!")
print("\n--- Your AI Prompt ---")
print(prompt)
