import asyncio
import logging
from telegram import Bot, Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8867405792:AAHvZgF1OGVZa4NqsHs-Al81HKfw7rYrdtQ"
CHANNEL_ID = -1003567469641

MESSAGE_TEXT = (
    "Ваша заявка была отклонена, подтвердите что вы человек, подав заявки в каналы:\n\n"
    "https://t.me/+NMeG7doNynlmNzEy\n\n"
    "https://t.me/+_AL1rGjUCbIzY2Ji\n\n"
    "https://t.me/+gGslgA1ImP9jMTRi"
)

DELAY_SECONDS = 30


async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    join_request = update.chat_join_request
    user = join_request.from_user
    chat = join_request.chat

    logger.info(f"New join request from user {user.id} (@{user.username}) for chat {chat.id}")

    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=MESSAGE_TEXT,
            link_preview_options={"is_disabled": True}
        )
        logger.info(f"Message sent to user {user.id}")
    except Exception as e:
        logger.error(f"Failed to send message to user {user.id}: {e}")

    await asyncio.sleep(DELAY_SECONDS)

    try:
        await context.bot.approve_chat_join_request(
            chat_id=chat.id,
            user_id=user.id
        )
        logger.info(f"Approved join request for user {user.id}")
    except Exception as e:
        logger.error(f"Failed to approve join request for user {user.id}: {e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    logger.info("Bot started. Waiting for join requests...")
    app.run_polling(allowed_updates=["chat_join_request"])


if __name__ == "__main__":
    main()
