from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

from chatbot.utils import strings

SWITCH_CHAT = range(1)


async def _switch_chat_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chatbot = ctx.user_data['chatbot']

    if not chatbot.chats:
        await update.message.reply_text(strings.NO_CHATS)
        return ConversationHandler.END

    await update.message.reply_text(
        strings.SWITCH_CHAT,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(chat_name, callback_data=f'switch:{chat_name}')]
                for chat_name in chatbot.chats
            ]
        ),
    )
    return SWITCH_CHAT


async def _switch_chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chatbot = ctx.user_data['chatbot']
    query = update.callback_query
    chat_name = query.data[7:]
    chatbot.current_chat = chat_name

    await query.edit_message_text(
        strings.SWITCHED_CHAT.format(chat_name=chat_name), parse_mode=ParseMode.HTML
    )
    await query.answer()

    return ConversationHandler.END


switch_chat_handler = ConversationHandler(
    entry_points=[CommandHandler('switchchat', _switch_chat_handler)],
    states={SWITCH_CHAT: [CallbackQueryHandler(_switch_chat, pattern='^switch:.+')]},
    fallbacks=[],
)
