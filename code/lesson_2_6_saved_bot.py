"""
Task 2.6: Saved Bot for Sweet Crumbs Bakery.

This chatbot reads business information from faq.json,
remembers conversations, saves chat history and handles errors.
"""

import json
import os

import httpx
import ollama

from langchain.chat_models import init_chat_model


# File names used by the chatbot.
FAQ_FILE = "faq.json"
HISTORY_FILE = "chat_history.json"
ERROR_FILE = "errors.log"


# Why: Business facts are kept in JSON so the owner can update them easily.
try:
    with open(FAQ_FILE, "r", encoding="utf-8") as file:
        faq = json.load(file)

except FileNotFoundError:
    print("FAQ file is missing. Please create faq.json first.")
    raise SystemExit


# Build the system message using the business information.
system_prompt = (
    f"You are the customer support assistant for "
    f"{faq.get('business_name', 'our business')}.\n"
    f"Here are the official business facts:\n"
    f"{json.dumps(faq, indent=2, ensure_ascii=False)}\n"
    "Answer customer questions using these facts only. "
    "Do not invent prices, services or policies. "
    "If information is not available, say you do not know."
)


# Create the AI model once.
model = init_chat_model(
    "llama3.2:latest",
    model_provider="ollama",
    temperature=0.2
)


def load_history() -> list[dict]:
    """Load previous chat messages from the history file."""

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

        # Why: Validate the file so damaged or incorrect data does not crash the bot.
        if not isinstance(history, list):
            raise ValueError("History must be a list.")

        for message in history:
            if (
                not isinstance(message, dict)
                or message.get("role") not in ["user", "assistant"]
                or not isinstance(message.get("content"), str)
            ):
                raise ValueError("Invalid message format.")

        print(f"Loaded {len(history)} old messages.")

        return history

    except (json.JSONDecodeError, ValueError, TypeError):
        print("History file was damaged. Starting a fresh chat.")
        return []


def save_history(history: list[dict]) -> None:
    """Save chat history as readable JSON."""

    # Why: Saving after every turn protects the conversation from being lost.
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=2,
            ensure_ascii=False
        )


def log_error(error: Exception) -> None:
    """Append an error message to errors.log."""

    with open(ERROR_FILE, "a", encoding="utf-8") as file:
        file.write(f"{type(error).__name__}: {error}\n")


def reset_history(history: list[dict]) -> None:
    """Clear the conversation and save an empty history."""

    history.clear()
    save_history(history)

    print("Bot: Chat history has been reset.")


def export_history(history: list[dict]) -> None:
    """Export the conversation as a readable text transcript."""

    with open("transcript.txt", "w", encoding="utf-8") as file:
        for message in history:
            file.write(
                f"{message['role']}: {message['content']}\n"
            )

    print("Bot: Chat exported to transcript.txt.")


def main() -> None:
    """Run the saved bakery chatbot."""

    history = load_history()

    print("\nSweet Crumbs Bot: Ask me anything.")
    print("Commands: /reset, /export, bye")

    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() == "bye":
            print("Bot: Goodbye! Your chat is saved.")
            save_history(history)
            break

        elif user_input.lower() == "/reset":
            reset_history(history)
            continue

        elif user_input.lower() == "/export":
            export_history(history)
            continue

        elif not user_input:
            print("Bot: Please enter a message.")
            continue

        # Add the customer's message to the history.
        history.append({
            "role": "user",
            "content": user_input
        })

        save_history(history)

        # Convert saved dictionaries into messages for the AI model.
        messages = [
            ("system", system_prompt)
        ]

        for message in history:
            role = "human" if message["role"] == "user" else "assistant"

            messages.append((
                role,
                message["content"]
            ))

        try:
            response = model.invoke(messages)

            answer = response.text

            history.append({
                "role": "assistant",
                "content": answer
            })

            save_history(history)

            print("Bot:", answer)

        except httpx.ConnectError as error:

            # Remove the unanswered question so failed messages are not remembered.
            history.pop()
            save_history(history)

            log_error(error)

            print(
                "Bot: I am offline right now. "
                "Please open the Ollama app and try again."
            )

        except ollama.ResponseError as error:

            history.pop()
            save_history(history)

            log_error(error)

            print(
                "Bot: I could not process your request. "
                "Please try again."
            )


if __name__ == "__main__":
    main()