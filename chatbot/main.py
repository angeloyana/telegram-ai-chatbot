from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, PicklePersistence

from chatbot.config import settings
from chatbot.handlers import (
    chats_handler,
    new_chat_handler,
    prompt_handler,
    start_handler,
    switch_chat_handler,
)
from chatbot.utils.logger import logger


async def error_handler(_, ctx: ContextTypes.DEFAULT_TYPE):
    logger.error('An exception was raised:', exc_info=ctx.error)


def main() -> None:
    persistence = PicklePersistence(settings.PERSISTENCE_FILEPATH)
    app = (
        ApplicationBuilder()
        .token(settings.BOT_TOKEN.get_secret_value())
        .persistence(persistence)
        .build()
    )

    app.add_error_handler(error_handler)
    app.add_handler(start_handler)
    app.add_handler(chats_handler)
    app.add_handler(new_chat_handler)
    app.add_handler(switch_chat_handler)
    app.add_handler(prompt_handler)

    app.run_polling(allowed_updates=[Update.CALLBACK_QUERY, Update.MESSAGE])


if __name__ == '__main__':
    main()
