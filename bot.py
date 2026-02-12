import logging
import os
import random
from typing import Final

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

STARTING_POINTS: Final[int] = 1000
HIT_REWARD: Final[int] = 200
HIT_PENALTY: Final[int] = 50

# In-memory points store: {user_id: points}
player_points: dict[int, int] = {}


def _get_points(user_id: int) -> int:
    if user_id not in player_points:
        player_points[user_id] = STARTING_POINTS
    return player_points[user_id]


def _set_points(user_id: int, points: int) -> None:
    player_points[user_id] = max(points, 0)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    if not update.effective_user or not update.message:
        return

    user = update.effective_user
    points = _get_points(user.id)
    await update.message.reply_text(
        (
            f"Namaste {user.first_name}! 🎮\n\n"
            "Main tumhara Gaming Bot hoon.\n"
            "Tumhare paas start me 1000 points hote hain.\n\n"
            "Commands:\n"
            "• /balance - Apne points dekho\n"
            "• /toss [amount] [H/T] - Coin toss game\n"
            "  Example: /toss 100 H\n"
            "• /hit [1-5] - Target hit game\n"
            "  Sahi guess = +200, galat = -50\n"
            "• /help - Command guide\n\n"
            f"Current Balance: {points}"
        )
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    if not update.message:
        return
    await update.message.reply_text(
        "Game Commands:\n"
        "/balance\n"
        "/toss [amount] [H/T]\n"
        "/hit [1-5]\n\n"
        "Toss me jeetoge to amount ka double milta hai (net +amount)."
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    if not update.effective_user or not update.message:
        return
    points = _get_points(update.effective_user.id)
    await update.message.reply_text(f"💰 Tumhara balance: {points} points")


async def toss(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id
    points = _get_points(user_id)

    if len(context.args) != 2:
        await update.message.reply_text("Use: /toss [amount] [H/T]\nExample: /toss 100 H")
        return

    amount_text, choice_text = context.args

    try:
        amount = int(amount_text)
    except ValueError:
        await update.message.reply_text("Amount number me do. Example: /toss 100 H")
        return

    if amount <= 0:
        await update.message.reply_text("Amount 0 se bada hona chahiye.")
        return

    if amount > points:
        await update.message.reply_text(
            f"Itne points nahi hain. Tumhara current balance: {points}"
        )
        return

    choice = choice_text.strip().upper()
    if choice not in {"H", "T"}:
        await update.message.reply_text("Choice sirf H ya T ho sakta hai.")
        return

    result = random.choice(["H", "T"])
    result_text = "Heads ✋🏻" if result == "H" else "Tails 👌🏻"

    if choice == result:
        new_points = points + amount
        _set_points(user_id, new_points)
        await update.message.reply_text(
            f"{result_text}\n🎉 Jeet gaye! +{amount} points\n"
            f"Naya Balance: {new_points}"
        )
    else:
        new_points = points - amount
        _set_points(user_id, new_points)
        await update.message.reply_text(
            f"{result_text}\n😢 Haar gaye! -{amount} points\n"
            f"Naya Balance: {new_points}"
        )


async def hit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id
    points = _get_points(user_id)

    if len(context.args) != 1:
        await update.message.reply_text("Use: /hit [1-5]\nExample: /hit 3")
        return

    try:
        guess = int(context.args[0])
    except ValueError:
        await update.message.reply_text("1 se 5 tak number do. Example: /hit 3")
        return

    if guess < 1 or guess > 5:
        await update.message.reply_text("Guess 1 se 5 ke beech hona chahiye.")
        return

    target = random.randint(1, 5)

    if guess == target:
        new_points = points + HIT_REWARD
        _set_points(user_id, new_points)
        await update.message.reply_text(
            f"🎯 Bullseye! Target {target} tha.\n"
            f"+{HIT_REWARD} points mile!\n"
            f"Naya Balance: {new_points}"
        )
    else:
        new_points = points - HIT_PENALTY
        _set_points(user_id, new_points)
        await update.message.reply_text(
            f"❌ Miss! Target {target} tha.\n"
            f"-{HIT_PENALTY} points cut gaye.\n"
            f"Naya Balance: {new_points}"
        )


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN environment variable missing. "
            "Set token before running bot."
        )

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("toss", toss))
    application.add_handler(CommandHandler("hit", hit))

    logger.info("Gaming bot is starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
