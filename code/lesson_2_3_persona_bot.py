"""A bakery AI assistant with different personas and verified menu prices."""

from langchain.chat_models import init_chat_model


# These are the verified facts the assistant is allowed to use.
facts = {
    "name": "Sweet Crumbs Bakery",
    "type": "Bakery",
    "city": "Lahore",
    "opening_hours": "9 AM to 10 PM",
    "delivery": "Delivery is available in Lahore",
    "speciality": "Fresh cakes and bakery items",
    "prices": {
        "cupcake": 250,
        "brownie": 300,
        "chocolate cake": 1500,
    },
}

# Personas let the user choose the assistant's communication style.
personas = {
    "friendly": "Speak warmly and casually. Be welcoming and helpful.",
    "formal": "Speak professionally and politely. Avoid casual language.",
    "sales": "Speak enthusiastically and encourage customers to explore our products.",
}

# Central configuration makes it easier to adjust model settings.
config = {
    "model": "llama3.2:latest",
    "temperature": 0.2,
    "memory_size": 8,
}

current_persona = "friendly"


def build_system_message(persona_name):
    """Build a system message using the business facts and chosen persona."""

    persona_style = personas.get(
        persona_name,
        "Speak clearly, politely, and helpfully.",
    )

    # Using the facts dictionary keeps business details in one place.
    return {
        "role": "system",
        "content": (
            f"You are the assistant for {facts['name']}.\n"
            f"Business facts: {facts}\n"
            f"Your communication style: {persona_style}\n"
            "Only use the business facts provided above. "
            "If a detail is missing, say you do not know. "
            "Never invent products, prices, or business information."
        ),
    }


def main():
    """Run the bakery assistant and handle chat commands."""

    llm = init_chat_model(
        config["model"],
        model_provider="ollama",
        temperature=config["temperature"],
    )

    current_persona = "friendly"
    messages = [build_system_message(current_persona)]

    print(f"{facts['name']} AI Assistant")
    print("Commands: /persona <name>, /price <item>, /add <item> <price>, bye")
    print("Available personas: friendly, formal, sales")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "bye":
            print("Assistant: Goodbye! Thanks for visiting Sweet Crumbs Bakery.")
            break

        elif user_input.lower().startswith("/persona "):
            requested_persona = user_input.split(maxsplit=1)[1].strip().lower()

            if requested_persona in personas:
                current_persona = requested_persona
                messages[0]["content"] = build_system_message(
                    current_persona
                )["content"]
                print(f"Assistant: Persona changed to {current_persona}.")
            else:
                # .get() provides a safe default instead of raising a KeyError.
                style = personas.get(
                    requested_persona,
                    "Speak clearly, politely, and helpfully.",
                )
                if requested_persona in personas:
                    print(f"Assistant: {style}")
                else:
                    print(
                        "Assistant: Unknown persona. Choose friendly, formal, or sales."
                    )

        elif user_input.lower().startswith("/price "):
            item = user_input.split(maxsplit=1)[1].strip().lower()

            # Dictionary lookup returns the official price without asking the AI.
            price = facts["prices"].get(item)

            if price is not None:
                print(f"Assistant: {item.title()} costs {price} PKR.")
            else:
                print(
                    f"Assistant: Sorry, {item} is not on our menu."
                )

        elif user_input.lower().startswith("/add "):
            parts = user_input.split(maxsplit=2)

            if len(parts) != 3:
                print("Assistant: Use this format: /add item price")
                continue

            item = parts[1].strip().lower()

            try:
                price = int(parts[2])
                if price < 0:
                    print("Assistant: Price cannot be negative.")
                    continue
            except ValueError:
                print("Assistant: Please enter the price as a whole number.")
                continue

            facts["prices"][item] = price

            # Rebuild the system message so the AI can use the updated facts.
            messages[0]["content"] = build_system_message(
                current_persona
            )["content"]

            print(f"Assistant: Added {item.title()} for {price} PKR.")

        elif user_input == "":
            print("Assistant: Please enter a message or command.")

        else:
            # Save both sides of the conversation to give the AI context.
            messages.append({"role": "user", "content": user_input})

            response = llm.invoke(messages)

            messages.append(
                {"role": "assistant", "content": response.text}
            )

            print("Assistant:", response.text)

            # Keep the system message plus the latest messages to limit memory.
            messages = [
                messages[0]
            ] + messages[1:][-config["memory_size"]:]


if __name__ == "__main__":
    main()
