# Task 2.6: Saved Bot

Business: Sweet Crumbs Bakery

## Files Created

- faq.json
- lesson_2_6_saved_bot.py
- .gitignore

## Features Implemented

1. Business information is loaded from faq.json.
2. Chat history is loaded from chat_history.json.
3. Chat history is saved after every turn.
4. Damaged history files are handled.
5. Connection and response errors are handled.
6. Errors are recorded in errors.log.
7. /reset clears the chat history.
8. /export creates a readable transcript.

## Testing Results

- FAQ loading: Passed
- Business information questions: Passed
- Price questions: Passed
- Chat history saving: Passed
- Previous conversation memory: Passed
- Reset command: Passed
- Export command: Passed
- Damaged history handling: Passed
- Ollama connection error handling: Passed

## Conclusion

The Saved Bot successfully uses JSON files to store business information and customer conversations. It also handles errors with friendly messages and protects private data through .gitignore.