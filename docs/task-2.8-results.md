Task 2.8: First AI Agent for Sweet Crumbs Bakery

Objective

The objective of this task was to build a simple AI agent that can check bakery prices, check order status, and place customer orders after owner approval.

Tools Created

1. get_price: Checks the price of bakery items.
2. order_status: Checks the status of customer orders.
3. place_order: Places a new order after owner approval.

Testing Results

Test 1: Price Comparison

Asked the agent to compare brownie and cupcake prices.

Result:
- Brownie: 300 PKR
- Cupcake: 250 PKR

The agent selected the correct tool and returned both prices.

Test 2: Order Status

Asked about order A102.

Result:
Order A102 is out for delivery.

The agent correctly used the order_status tool.

Test 3: Place Order

Customer: Ali
Item: 2 Brownies
Total: 600 PKR

Owner Approval: Yes

Result:
Order A104 was successfully placed.

Test 4: Cancel Order

Customer: Sara
Item: 1 Cupcake
Total: 250 PKR

Owner Approval: No

Result:
The order was cancelled because the owner did not approve it.

Test 5: Conversation Memory

Asked: What is my name?

Result:
The agent correctly remembered the name Sara.

Tool Selection Accuracy

Total tool calls: 5
Correct tool selections: 5
Accuracy: 100%

Conclusion

The AI agent successfully completed all the main tests. It checked prices, retrieved order status, placed orders after approval, handled cancelled orders, and remembered information during the conversation.