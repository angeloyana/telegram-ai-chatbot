from telegram import Update
from telegram.ext import filters, ContextTypes, MessageHandler

from chatbot.utils import strings


async def _prompt_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chatbot = ctx.user_data['chatbot']
    chat_name = chatbot.current_chat
    if not chat_name:
        await update.message.reply_text(strings.NO_CHAT)
        return

    chat = chatbot.chats[chat_name]
    prompt = update.message.text

    await update.message.reply_chat_action('typing')
    response = await chat.send_message_async(prompt)
    await update.message.reply_text(response.text)


prompt_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, _prompt_handler)
