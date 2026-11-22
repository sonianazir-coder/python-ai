Task 2.7: Hallucination Hunt

Project: Sweet Crumbs Bakery Order Extractor

1. Off-menu item test

Input: 1 pizza and 2 brownies, Bilal, Model Town

Result: The AI extracted both items. Python checked the menu and identified pizza as an unavailable item.

CHECK: 'pizza' is not on the menu.

2. Missing customer name test

Input: Please send 2 cupcakes to Lahore.

Result: The customer name was not provided in the original message. The program checks whether the extracted name exists in the original message and flags an invented name.

3. Non-order message test

Input: Hi, do you deliver to Johar Town?

Result: The program identified that this was a question, not an order. It printed that a human reply was needed.

4. Roman Urdu test

Input: Mujhe 3 brownies chahiye. Mera naam Ahmed hai, address DHA Lahore.

Result: The AI successfully extracted the customer name, address, item and quantity.

5. Price calculation test

The program calculated prices using the Python PRICES dictionary instead of trusting AI-generated prices.

Conclusion:

The Order Extractor successfully processed English and Roman Urdu messages. Menu validation identified unavailable items, and Python calculated the order totals. These checks help reduce incorrect information in business records.