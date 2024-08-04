from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    filters,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
)

from chatbot.genai import model
from chatbot.utils import strings

GET_CHAT_NAME, SWITCH_CHAT = range(2)


async def _new_chat_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(strings.NEW_CHAT)
    return GET_CHAT_NAME


async def _get_chat_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chatbot = ctx.user_data['chatbot']
    chat_name = update.message.text
    if not chat_name:
        await update.message.reply_text(strings.CHAT_NAME_INVALID)
        return GET_CHAT_NAME

    if chat_name in chatbot.chats:
        await update.message.reply_html(
            strings.CHAT_NAME_EXISTS.format(chat_name=chat_name)
        )
        return GET_CHAT_NAME

    chatbot.chats[chat_name] = model.start_chat(history=[])
    await update.message.reply_html(
        strings.NEW_CHAT_DONE.format(chat_name=chat_name),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Yes', callback_data=f'yes:{chat_name}'),
                    InlineKeyboardButton('No', callback_data=f'no:{chat_name}'),
                ]
            ]
        ),
    )
    return SWITCH_CHAT


async def _switch_chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chatbot = ctx.user_data['chatbot']
    query = update.callback_query
    choice, chat_name = query.data.split(':', 1)

    if choice == 'yes':
        chatbot.current_chat = chat_name
        await query.edit_message_text(
            strings.SWITCHED_CHAT.format(chat_name=chat_name), parse_mode=ParseMode.HTML
        )
    else:
        await query.delete_message()

    await query.answer()
    return ConversationHandler.END


new_chat_handler = ConversationHandler(
    entry_points=[CommandHandler('newchat', _new_chat_handler)],
    states={
        GET_CHAT_NAME: [MessageHandler(filters.ALL, _get_chat_name)],
        SWITCH_CHAT: [CallbackQueryHandler(_switch_chat, pattern='^(yes|no):.+')],
    },
    fallbacks=[],
)
