import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from main import create_card
from dotenv import dotenv_values

secrets = dotenv_values(".env")
TRELLO_API_KEY = secrets["TRELLO_API_KEY"]
TELEGRAM_API_TOKEN = secrets["TELEGRAM_API_TOKEN"]
TRELLO_API_TOKEN = secrets["TRELLO_API_TOKEN"]
TASK_BOARD_ID = "662d460176109a20d3096508"
TASK_LIST_ID = "662d460176109a20d3096508"
SHOPPING_LIST_ID = "662d4c92d429bc9420681a3e"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

#Command Handlers Functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hi!")

async def add_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a card to the corresponding board when the command /card [board] card_name is issued."""
    board = context.args[0] 
    user_message = " ".join(context.args[1:]).capitalize()
   
    if user_message:
        ADD_CARD_COMMAND_PATHS = {
        "s": {"id": SHOPPING_LIST_ID, "success": f'"{user_message}" añadido al carro', "error": f"Error añadiendo al carro: {user_message}"},
        "t": {"id": TASK_LIST_ID, "success": f'Tarea: "{user_message}" creada correctamente', "error": f"Error creando tarea: {user_message}"},
        } 
        create_card_response = await create_card(ADD_CARD_COMMAND_PATHS[board]["id"], TRELLO_API_KEY,TRELLO_API_TOKEN, name=user_message)
        if create_card_response == True:        
            await update.message.reply_text(ADD_CARD_COMMAND_PATHS[board]["success"])
        else:
            await update.message.reply_text(ADD_CARD_COMMAND_PATHS[board]["error"])
            #print(create_card_response)
    else:
        await update.message.reply_text('Please provide text after the command.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("card", add_card))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()