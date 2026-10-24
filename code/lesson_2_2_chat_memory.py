"""A personal AI tutor that remembers messages during a conversation."""

from langchain.chat_models import init_chat_model


def main():
    """Run the tutor and manage conversation memory."""

    # A system message defines the tutor's role and keeps its replies concise.
    system_message = {
        "role": "system",
        "content": (
            "You are a helpful personal tutor. Give clear, simple answers "
            "in about 2-4 sentences. Use the conversation to remember "
            "relevant details shared by the user."
        ),
    }

    messages = [system_message]

    # This second list records user questions separately for the stretch task.
    questions = []

    # The model is created once so it does not need to be initialized each turn.
    llm = init_chat_model(
        "llama3.2:latest",
        model_provider="ollama",
        temperature=0.2,
    )

    print("Tutor: Ask me anything. Commands: /reset, /count, bye")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "bye":
            print("Tutor: Goodbye!")
            print(f"Questions asked: {len(questions)}")

            if questions:
                print("First question:", questions[0])
                print("Last question:", questions[-1])
            else:
                print("No questions were asked.")

            break

        elif user_input.lower() == "/reset":
            # Keep the system message so the tutor retains its role after reset.
            messages = [messages[0]]
            print("Tutor: Memory cleared.")

        elif user_input.lower() == "/count":
            print(f"Tutor: {len(messages)} messages in memory.")

        elif user_input == "":
            print("Tutor: Please enter a message.")

        else:
            questions.append(user_input)

            # Both sides of the conversation are saved so the AI can use context.
            messages.append({"role": "user", "content": user_input})

            response = llm.invoke(messages)

            messages.append(
                {"role": "assistant", "content": response.text}
            )

            print("Tutor:", response.text)

            # Only the system message and the latest 8 other messages are retained.
            messages = [messages[0]] + messages[1:][-8:]

            # Input tokens show how much conversation context was sent to the model.
            tokens_sent = response.usage_metadata["input_tokens"]
            print(f"(tokens sent: {tokens_sent})")


if __name__ == "__main__":
    main()
