from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from utils.tg import start, restart, echo
from config import TG_BOT_API_KEY

def main() -> None:
    # Create the Application and pass it your bot's token
    token = TG_BOT_API_KEY
    application = Application.builder().token(token).build()

    # Register handlers for different commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("restart", restart))
    # Message handler for all text (non-command) messages to use OpenAI
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()