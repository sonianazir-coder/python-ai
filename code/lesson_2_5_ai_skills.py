"""
Task 2.5: AI Skills Toolkit for Sweet Crumbs Bakery.

This toolkit provides reusable AI skills for summarizing,
translating messages, replying to reviews, and estimating tokens.
"""

from langchain.chat_models import init_chat_model


# Why: Models are created once so we can reuse them instead of creating them repeatedly.
precise_model = init_chat_model(
    "llama3.2:latest",
    model_provider="ollama",
    temperature=0.2
)

creative_model = init_chat_model(
    "llama3.2:latest",
    model_provider="ollama",
    temperature=0.8
)


def ask_ai(
    prompt: str,
    system: str = "You are a helpful bakery assistant.",
    creative_mode: bool = False
) -> str:
    """Send a prompt to the selected AI model and return its text."""

    # Why: Different tasks need different response styles.
    model = creative_model if creative_mode else precise_model

    response = model.invoke([
        ("system", system),
        ("human", prompt)
    ])

    return response.text


def summarize(text: str) -> str:
    """Summarize customer feedback for Sweet Crumbs Bakery."""

    system = "You summarize customer feedback clearly and briefly."

    prompt = f"Summarize this customer feedback in 2 lines:\n{text}"

    return ask_ai(prompt, system)


def translate(text: str, language: str = "Urdu") -> str:
    """Translate bakery messages into the selected language."""

    system = "You are a professional translator."

    prompt = f"Translate this message into {language}:\n{text}"

    return ask_ai(prompt, system)


def reply_to_review(review: str) -> str:
    """Write a friendly reply to a Sweet Crumbs Bakery review."""

    system = (
        "You are the customer support assistant of Sweet Crumbs Bakery. "
        "Write polite, friendly and professional replies."
    )

    prompt = f"Write a reply to this customer review:\n{review}"

    return ask_ai(prompt, system, creative_mode=True)


def estimate_tokens(text: str) -> int:
    """Estimate the number of tokens in a text without using AI."""

    return max(1, len(text.split()))


# Why: Assertions check our normal Python function without spending AI tokens.
assert estimate_tokens("Hello bakery customer") == 3
assert estimate_tokens("Sweet Crumbs Bakery Lahore") == 4


# Count how many times each skill is used.
usage = {
    "summarize": 0,
    "translate": 0,
    "reply": 0,
    "tokens": 0
}


print("Sweet Crumbs AI Toolkit")
print("Commands: /summarize, /translate, /reply, /tokens, bye")


while True:

    command = input("\nCommand: ").strip().lower()

    if command == "bye":

        print("\nSkills used today:")

        for skill, count in usage.items():
            print(f"  {skill}: {count}")

        print("Goodbye!")

        break

    elif command == "/summarize":

        text = input("Customer feedback: ")

        result = summarize(text)

        usage["summarize"] += 1

        print("AI:", result)

    elif command == "/translate":

        text = input("Text to translate: ")

        language = input("Language (Enter for Urdu): ").strip()

        # Why: An empty input uses Urdu automatically as the default language.
        if language == "":
            language = "Urdu"

        result = translate(text, language)

        usage["translate"] += 1

        print("AI:", result)

    elif command == "/reply":

        review = input("Customer review: ")

        result = reply_to_review(review)

        usage["reply"] += 1

        print("AI:", result)

        print(f"(Review was about {estimate_tokens(review)} tokens)")

    elif command == "/tokens":

        text = input("Enter text: ")

        count = estimate_tokens(text)

        usage["tokens"] += 1

        print(f"Estimated tokens: {count}")

    else:

        print(
            "Unknown command. "
            "Try /summarize, /translate, /reply, /tokens or bye."
        )