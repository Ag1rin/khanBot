# General Telegram Bot with OpenAI Integration

This is a customizable Telegram bot built using the `python-telegram-bot` library and integrated with OpenAI's GPT-4 for intelligent product consultations. It includes features like forced channel membership checks, inline and persistent keyboards, admin notifications for consultation requests, and AI-powered responses.

## Features

* Forced Channel Join: Users must join a specified channel to interact with the bot.
* Inline Buttons: Quick links to view products or request phone consultations.
* Persistent Keyboard: Always-visible buttons for consultations, products, and help.
* Admin Notifications: Forwards user contact details to an admin for phone consultations.
* AI Consultation: Uses OpenAI to provide personalized product recommendations based on user queries.
* Logging: Basic logging for errors and info to aid debugging.
* Error Handling: Improved try-except blocks to handle API failures gracefully.

## Prerequisites

* Python 3.6+
* Install dependencies: `pip install python-telegram-bot openai`

## Setup

1. **Tokens and IDs**:
   * Replace `TELEGRAM_BOT_TOKEN` with your bot token from BotFather.
   * Replace `OPENAI_API_KEY` with your OpenAI API key.
   * Set `ADMIN_ID` to your Telegram user ID (for receiving notifications).
   * Set `FORCE_JOIN_CHANNEL` to your channel username (e.g., `@my_channel`).

2. **Customization**:
   * Update URLs in buttons and messages to point to your website or channel.
   * Modify the OpenAI system prompt to fit your product domain (e.g., laptops, gadgets).
   * Add more handlers or buttons as needed for expansion.

3. **Running the Bot**:
   ```bash
   python your_bot_script.py
   ```
   The bot will start polling and log "✅ Bot is running."

## Expansion Ideas

* Database Integration: Add SQLite or MongoDB to store user queries or consultation logs.
* More Commands: Implement `/help`, `/products`, or custom commands.
* Rate Limiting: Prevent spam by limiting API calls per user.
* Multi-Language Support: Detect user language and respond accordingly.
* Webhooks: Switch from polling to webhooks for production deployment.

## Notes

* This bot is designed to be general-purpose. Adapt the AI prompt and buttons for any e-commerce or consultation service.
* Ensure compliance with Telegram's and OpenAI's terms of service.
* For production, use environment variables for sensitive keys (e.g., via `os.getenv`).

If you encounter issues, check the logs for details. Contributions welcome! 🚀
