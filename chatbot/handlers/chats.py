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

from chatbot.utils import strings

CHAT_OPTIONS, DELETE_CHAT, HANDLE_OPTIONS, RENAME_CHAT = range(4)


async def _chats_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chatbot = ctx.user_data['chatbot']

    if not chatbot.chats:
        await update.message.reply_text(strings.NO_CHATS)
        return ConversationHandler.END

    await update.message.reply_text(
        strings.LIST_CHATS,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(chat_name, callback_data=f'options:{chat_name}')]
                for chat_name in chatbot.chats
            ]
        ),
    )

    return CHAT_OPTIONS


async def _chat_options(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chatbot = ctx.user_data['chatbot']
    query = update.callback_query
    chat_name = query.data[8:]

    await query.edit_message_text(
        strings.VIEW_CHAT.format(
            chat_name=chat_name, total_messages=len(chatbot.chats[chat_name].history)
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Rename', callback_data=f'rename:{chat_name}'),
                    InlineKeyboardButton('Use', callback_data=f'switch:{chat_name}'),
                    InlineKeyboardButton('Delete', callback_data=f'delete:{chat_name}'),
                ],
                [InlineKeyboardButton('Back', callback_data=f'back:{chat_name}')],
            ]
        ),
    )

    return HANDLE_OPTIONS


async def _handle_options(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        chatbot = ctx.user_data['chatbot']
        query = update.callback_query
        option, chat_name = query.data.split(':', 1)

        if option == 'rename':
            ctx.user_data['previous_chat_name'] = chat_name
            await query.edit_message_text(strings.RENAME_CHAT)
            return RENAME_CHAT

        if option == 'switch':
            await query.edit_message_text(
                strings.SWITCHED_CHAT.format(chat_name=chat_name),
                parse_mode=ParseMode.HTML,
            )
            return ConversationHandler.END

        if option == 'delete':
            await query.edit_message_text(
                strings.DELETE_CHAT.format(chat_name=chat_name),
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                'Yes', callback_data=f'yes:{chat_name}'
                            ),
                            InlineKeyboardButton('No', callback_data=f'no:{chat_name}'),
                        ]
                    ]
                ),
            )
            return DELETE_CHAT

        await query.edit_message_text(
            strings.LIST_CHATS,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            chat_name, callback_data=f'options:{chat_name}'
                        )
                    ]
                    for chat_name in chatbot.chats
                ]
            ),
        )

        return CHAT_OPTIONS
    finally:
        await query.answer()


async def _delete_chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chatbot = ctx.user_data['chatbot']
    query = update.callback_query
    choice, chat_name = query.data.split(':', 1)

    if choice == 'yes':
        current_chat = chatbot.current_chat
        chatbot.current_chat = current_chat if chat_name != current_chat else None
        del chatbot.chats[chat_name]

        await query.edit_message_text(
            strings.DELETE_CHAT_DONE.format(chat_name=chat_name),
            parse_mode=ParseMode.HTML,
        )
    else:
        await query.delete_message()

    await query.answer()
    return ConversationHandler.END


async def _rename_chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chatbot = ctx.user_data['chatbot']
    chat_name = ctx.user_data.pop('previous_chat_name')
    new_chat_name = update.message.text

    if not new_chat_name:
        await update.message.reply_text(strings.CHAT_NAME_INVALID)
        return RENAME_CHAT

    if new_chat_name in chatbot.chats:
        await update.message.reply_html(
            strings.CHAT_NAME_EXISTS.format(chat_name=chat_name)
        )
        return RENAME_CHAT

    chat = chatbot.chats.pop(chat_name)
    chatbot.chats[new_chat_name] = chat
    await update.message.reply_html(
        strings.RENAME_CHAT_DONE.format(
            chat_name=chat_name, new_chat_name=new_chat_name
        )
    )
    return ConversationHandler.END


chats_handler = ConversationHandler(
    entry_points=[CommandHandler('chats', _chats_handler)],
    states={
        CHAT_OPTIONS: [CallbackQueryHandler(_chat_options, pattern='^options:.+')],
        HANDLE_OPTIONS: [
            CallbackQueryHandler(
                _handle_options, pattern='^(back|delete|rename|switch):.+'
            )
        ],
        DELETE_CHAT: [CallbackQueryHandler(_delete_chat, pattern='^(yes|no):.+')],
        RENAME_CHAT: [MessageHandler(filters.ALL, _rename_chat)],
    },
    fallbacks=[],
)
