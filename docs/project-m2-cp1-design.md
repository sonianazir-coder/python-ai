# Module 2 Checkpoint 1: AI Content Studio

## Business Information

Business Name: Sweet Crumbs Bakery

Business Type: Bakery

City: Lahore

## 1. Facts

| Key | Value |
|---|---|
| name | Sweet Crumbs Bakery |
| city | Lahore |
| hours | 9 AM to 10 PM |
| delivery | Available in Lahore |
| delivery_fee | 200 PKR |
| free_delivery_minimum | 3000 PKR |
| speciality | Fresh cakes, cupcakes, and brownies |
| prices | Chocolate Cake: 1500 PKR, Cupcake: 250 PKR, Brownie: 300 PKR, Mango Tart: 0 PKR |

Mango Tart is coming soon.

## 2. Tones

| Tone | Description |
|---|---|
| fun | Playful, energetic, and friendly |
| premium | Elegant, calm, and focused on quality |
| urgent | Exciting and encouraging customers to order soon |

## 3. Model Selection

| Job | Model and Temperature | Why |
|---|---|---|
| Menu descriptions | Creative, 0.8 | Marketing descriptions should be attractive. |
| Social media posts | Creative, 0.8 | Different styles make posts more interesting. |
| Customer questions | Precise, 0.2 | Customer replies should be consistent. |
| Price lookup | No AI model | Prices must come from real business data. |

## 4. Feature Tests

| Test | Expected Result | Pass? |
|---|---|---|
| /menu | Numbered menu; Mango Tart skipped | Pass |
| /post fun | Fun social post |Pass |
| /post premium | Premium social post | Pass |
| /post urgent | Urgent social post | Pass |
| /post pirate | Default tone; no crash | Pass |
| /price CUPCAKE | Correct price | Pass |
| /price mango tart | Coming soon | Pass |
| /price pizza | Not on menu | Pass|
| Ask and recall a name | Name remembered | Pass |
| /reset | Conversation reset | Pass |
| Empty input | Asks again | Not tested |
| BYE | Goodbye and report | Pass |