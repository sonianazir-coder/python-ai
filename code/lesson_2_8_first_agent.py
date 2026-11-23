"""
Task 2.8: First AI Agent for Sweet Crumbs Bakery.

The agent checks prices, order status and places orders
after owner approval.
"""

import re

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.messages import SystemMessage, HumanMessage, ToolMessage
from pydantic import ValidationError


# Bakery menu and prices.
PRICES = {
    "cupcake": 250,
    "chocolate cake": 1500,
    "brownie": 300,
    "cookies": 200,
    "vanilla cake": 1200,
}

# Existing customer orders.
ORDERS = {
    "A102": "out for delivery",
    "A103": "being prepared",
}


# Tool 1: Check item price.
@tool(parse_docstring=True)
def get_price(item: str) -> str:
    """Get the price of a bakery item.

    Args:
        item: Name of the bakery item.
    """
    item = item.strip().lower()

    if item not in PRICES:
        return f"{item} is not available on our menu."

    return f"{item} costs {PRICES[item]} PKR"


# Tool 2: Check order status.
@tool(parse_docstring=True)
def order_status(order_id: str) -> str:
    """Check the status of a customer order.

    Args:
        order_id: Customer's order ID.
    """
    order_id = order_id.strip().upper()
    status = ORDERS.get(order_id)

    if status is None:
        return f"Order {order_id} was not found."

    return f"Order {order_id} is {status}"


# Tool 3: Place order after owner approval.
@tool(parse_docstring=True)
def place_order(item: str, quantity: int, customer: str) -> str:
    """Place a new bakery order after owner approval.

    Args:
        item: Name of the bakery item.
        quantity: Number of items.
        customer: Customer's name.
    """
    item = item.strip().lower()
    customer = customer.strip()

    if item not in PRICES:
        return f"{item} is not available."

    if quantity <= 0 or not customer:
        return "Invalid quantity or customer name."

    total = PRICES[item] * quantity

    # Why: Owner approval prevents unauthorized orders.
    approval = input(
        f"[approve] {quantity} x {item} for {customer} "
        f"= {total} PKR. Place it? (yes/no) "
    ).strip().lower()

    if approval != "yes":
        return "Order cancelled. Owner did not approve it."

    order_id = f"A{102 + len(ORDERS)}"
    ORDERS[order_id] = "being prepared"

    return f"Order {order_id} placed: {quantity} x {item}, total {total} PKR"


# All available tools.
TOOLS = {
    "get_price": get_price,
    "order_status": order_status,
    "place_order": place_order,
}


# Why: Temperature 0 gives more consistent answers.
model = init_chat_model(
    "llama3.2:latest",
    model_provider="ollama",
    temperature=0
)

model_with_tools = model.bind_tools(list(TOOLS.values()))

MAX_STEPS = 5


def run_agent(messages: list) -> str:
    """Run the agent and execute tool calls."""

    for step in range(MAX_STEPS):
        response = model_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return str(response.content)

        for call in response.tool_calls:
            name = call["name"]
            args = call["args"]
            tool_id = call["id"]

            if name not in TOOLS:
                result = f"Unknown tool: {name}"
            else:
                try:
                    result = TOOLS[name].invoke(args)
                except ValidationError:
                    result = "Invalid tool arguments."

            print(f"  [tool] {name}({args}) -> {result}")

            # Why: The ID connects the tool result to its request.
            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_id
                )
            )

    else:
        return "Maximum steps reached. Please try again."


def main() -> None:
    """Start the bakery agent with conversation memory."""

    messages = [
        SystemMessage(
            content=(
                "You are Sweet Crumbs Bakery's agent. "
                "Use tools for prices, order status and new orders. "
                "Trust tool results and never invent information. "
                "Report the exact order status returned by the tool. "
                "Only confirm an order when the tool says it was placed. "
                "If cancelled, clearly say it was cancelled. "
                "Remember customer names from conversation."
            )
        )
    ]

    remembered_name = None

    print("\nSweet Crumbs Agent: Ask about prices, orders, or place an order. Type 'bye' to exit.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "bye":
            print("Agent: Goodbye! Thanks for visiting Sweet Crumbs.")
            break

        if not user_input:
            continue

        # Save customer name from their message.
        match = re.search(
            r"\b(?:I am|my name is)\s+([A-Za-z]+)",
            user_input,
            re.IGNORECASE
        )

        if match:
            remembered_name = match.group(1)

        # Answer name questions from saved memory.
        if "what is my name" in user_input.lower():
            if remembered_name:
                print(f"Agent: Your name is {remembered_name}.")
            else:
                print("Agent: You have not told me your name yet.")
            continue

        messages.append(HumanMessage(content=user_input))
        answer = run_agent(messages)

        print(f"Agent: {answer}")


if __name__ == "__main__":
    main()