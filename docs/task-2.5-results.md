# Task 2.5: AI Skills Toolkit

Business: Sweet Crumbs Bakery

## Skills Implemented

1. summarize() - Summarizes customer feedback.
2. translate() - Translates messages into the selected language.
3. reply_to_review() - Generates friendly replies to customer reviews.
4. estimate_tokens() - Estimates tokens without using an AI model.

## Models

- Precise model: llama3.2:latest, temperature 0.2
- Creative model: llama3.2:latest, temperature 0.8

## Testing Results

- Translation command: Passed
- Review reply command: Passed
- Summary command: Passed
- Unknown command handling: Passed
- Token estimation assertions: Passed
- Usage report: Passed
- Default Urdu language: Passed
- Token estimation command: Passed

## Conclusion

The AI Skills Toolkit successfully runs reusable AI skills for Sweet Crumbs Bakery. It uses two models, functions, type hints, assertions, a menu loop and a usage dictionary.