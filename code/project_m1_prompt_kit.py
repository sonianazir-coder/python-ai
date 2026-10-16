"""Create three useful AI prompts for a local business."""

# Business details help make each prompt specific to the client's needs.
business = input("Business name: ")
business_type = input("Business type: ")
city = input("City: ")
customers = input("Main customers: ")

# Converting the budget to an integer allows the prompt to use a numeric amount.
budget = int(input("Monthly budget (PKR): "))

# A clear heading helps the user identify the generated prompt kit.
print("\n=========================================")
print(f"   AI Prompt Kit for {business}")
print("=========================================")

# Naming the audience helps AI create more relevant marketing content.
marketing_prompt = (
    f"Write a short Instagram post for {business}, "
    f"a {business_type} in {city}. "
    f"Target {customers}. Use a friendly tone and include 1 call to action."
)

# Giving AI a role and a clear task helps it produce a suitable customer reply.
service_prompt = (
    f"You are the manager of {business}. "
    "Write a polite reply to a customer whose order arrived late. "
    "Apologise and offer a small discount."
)

# Including the budget helps AI suggest ideas that fit the business's limits.
growth_prompt = (
    f"Suggest 3 low-cost AI tools a {business_type} in {city} can use "
    f"to attract {customers} with a budget of {budget} PKR per month."
)

print("\n[1] Marketing")
print(marketing_prompt)

print("\n[2] Customer Service")
print(service_prompt)

print("\n[3] Growth")
print(growth_prompt)