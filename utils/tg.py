import telegram
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils.parser import telegram_format
from utils.gpt import client, thread, assistant

# Define the keyboard buttons
keyboard = [
    ['Перезапустить', 'Помощь']
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message when the command /start is issued
    await update.message.reply_text(
        "Добрый день! Чем могу помочь?",
        reply_markup=reply_markup
    )

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global thread
    # Delete the existing thread
    client.beta.threads.delete(thread.id)
    # Create a new thread
    thread = client.beta.threads.create()
    await update.message.reply_text(
        "Я перезапустился и все забыл!", 
        reply_markup=reply_markup)
    return thread
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == "Перезапустить":
        await restart(update, context)
        return
    if update.message.text == "Помощь":
        await update.message.reply_text(
                "Инcтрукция как пользоваться ботом: ___", 
                reply_markup=reply_markup)
        return
    
    # Take user message and use OpenAI to generate a response
    input_text = update.message.text

    # Create message in the existing thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=input_text
    )
    
    # Show TYPING

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=telegram.constants.ChatAction.TYPING
    )

    # Run the assistant and wait for completion
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    if run.status == 'completed':
        # Retrieve all thread messages
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        if messages.data:
            response = telegram_format(messages.data[0].content[0].text.value)
            await update.message.reply_text(
                response, 
                parse_mode="HTML",
                reply_to_message_id=update.message.message_id,
                reply_markup=reply_markup)
    else:
        await update.message.reply_text(
            "Что-то пошло не так, перезапускаюсь!", 
            reply_markup=reply_markup)
        await restart(update, context)