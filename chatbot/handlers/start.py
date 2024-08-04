from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from chatbot.utils import get_full_name, strings
from chatbot.utils.schemas import Chatbot


async def _start_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if 'chatbot' not in ctx.user_data:
        ctx.user_data['chatbot'] = Chatbot()

    await update.message.reply_html(
        strings.START.format(
            user_name=update.effective_user.first_name, bot_name=get_full_name(ctx.bot)
        )
    )


start_handler = CommandHandler('start', _start_handler)
