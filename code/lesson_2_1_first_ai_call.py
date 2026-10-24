"""An AI tutor that explains a topic at the user's chosen level."""

import time

from langchain.chat_models import init_chat_model


def main():
    """Ask the user for a topic and level, then call the AI model."""

    topic = input("Enter a topic: ").strip()
    level = input("Enter your level (beginner/expert): ").strip().lower()

    # A system message controls the AI's role and the length of its answer.
    system_message = (
        f"You are a helpful AI tutor. Explain {topic} to a {level} student. "
        "Keep your answer clear and appropriate for the student's level."
    )

    # Temperature 0.2 makes responses more consistent for this learning task.
    model = init_chat_model(
        "llama3.2:latest",
        model_provider="ollama",
        temperature=0.2,
    )

    start_time = time.perf_counter()

    response = model.invoke(
        [
            ("system", system_message),
            ("human", f"Explain this topic: {topic}"),
        ]
    )

    elapsed_time = time.perf_counter() - start_time

    print("\nTopic:", topic)
    print("Level:", level)
    print("-" * 40)
    print(response.text)
    print("-" * 40)

    tokens = response.usage_metadata["total_tokens"]
    print(f"{tokens} tokens in {elapsed_time:.1f} seconds")


if __name__ == "__main__":
    main()
