# Telegram AI Chatbot

This is a basic personal AI Chatbot 🤖 that offers several features
including text-based prompting, multiple chat management, and persistent memory.

## Installation

```bash
# Clone this repository
git clone https://github.com/angeloyana/telegram-ai-chatbot

cd telegram-ai-chatbot

# You might also want to use virtualenv for isolating dependencies.
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Start the Chatbot

Before running the bot, this are the required environment variables:

```
BOT_TOKEN=<token>       # Get here: https://t.me/BotFather
GENAI_API_KEY=<api_key> # Get here: https://aistudio.google.com/app/apikey
```

Then run:

```bash
python -m chatbot.main
```

## License
This project is licensed under the [MIT License](./LICENSE)
