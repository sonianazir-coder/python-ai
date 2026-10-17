"""Lesson 1.6: Clean user text and build an AI prompt."""

# Ask the user for their name and question.
name = input("Enter your name: ")
question = input("Enter your question: ")

# strip() removes extra spaces; title() formats the name neatly.
clean_name = name.strip().title()

# capitalize() cleans the question's first letter.
clean_question = question.strip().capitalize()

# len() counts characters, and dividing by 4 estimates English tokens.
characters = len(clean_question)
estimated_tokens = round(characters / 4)

# lower() makes the Python check work with different capital letters.
mentions_python = "python" in clean_question.lower()

# Slicing limits the question to 150 characters.
short_question = clean_question[:150]

# An f-string inserts the cleaned values into the AI prompt.
prompt = f"""You are a helpful Python tutor.
Greet the user by name: {clean_name}.
Answer the user's question in 3 short lines.
User's question: {short_question}"""

print("\n" + "=" * 40)
print("PROMPT CLEANER RESULTS")
print("=" * 40)

print(f"Name: {clean_name}")
print(f"Cleaned question: {clean_question}")
print(f"Characters: {characters}")
print(f"Estimated tokens: {estimated_tokens}")
print(f"Mentions Python: {mentions_python}")

print("\n--- AI Prompt ---")
print(prompt)
print("=" * 40)