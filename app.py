import json
import time
import warnings
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.warnings import PTBUserWarning
from chatgpt_md_converter import telegram_format
from telegram.error import InvalidToken, BadRequest, Forbidden

# --- Suppress the specific warning ---
warnings.filterwarnings("ignore", category=PTBUserWarning)
# ------------------------------------

def exit_with_error(message, duration=5):
    """
    Prints a formatted error message, waits, and then exits the program.
    This is used for startup errors.
    """
    print("\n" + "="*50)
    print(message)
    print("="*50 + "\n")
    time.sleep(duration)
    exit()

class TelegramBot:
    """
    Main class for the bot, encapsulating all logic.
    """
    def __init__(self):
        """
        Initializes the bot by loading and validating the initial config.
        """
        print("Initializing bot...")
        try:
            self.config = self.load_config()
        except FileNotFoundError:
            # This error is fatal on startup
            exit_with_error(
                "Error: 'config.json' file not found.\n"
                "Please make sure 'config.json' is in the same folder as the .exe file."
            )
        
        # Validate critical startup config
        self.bot_token = self.config.get('BOT_TOKEN')
        self.channel_id = self.config.get('CHANNEL_ID') # For initial check
        
        if not self.bot_token:
            exit_with_error("Error: 'BOT_TOKEN' is empty in config.json. Please set it.")
        if not self.channel_id:
            exit_with_error("Error: 'CHANNEL_ID' is empty in config.json. Please set it.")
        
        print("Initial config loaded and validated.")

    def load_config(self):
        """
        Loads and returns the configuration from config.json.
        Raises FileNotFoundError if not found.
        """
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    async def reload_config_on_the_fly(self):
        """
        Reloads config.json. This is called by handle_message to get fresh
        CHANNEL_ID and MY_USER_ID values without restarting.
        Returns True on success, False on failure.
        """
        try:
            self.config = self.load_config()
            if not self.config.get('CHANNEL_ID'):
                 print("Error: 'CHANNEL_ID' is empty in reloaded config. Ignoring message.")
                 return False
            return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reloading config.json during runtime: {e}. Ignoring message.")
            return False

    async def _send_to_channel(self, context: ContextTypes.DEFAULT_TYPE, channel_id, html_text, update: Update):
        """
        Internal method to handle sending the message to the channel
        and capture any specific errors.
        """
        try:
            await context.bot.send_message(chat_id=channel_id, text=html_text, parse_mode="HTML")
            print(f"Successfully forwarded message to channel {channel_id}")
        
        except (BadRequest, Forbidden) as e:
            # This catches errors related to the channel (e.g., wrong ID, not admin)
            print(f"Error sending message to channel {channel_id}: {e}")
            print("Please check if the CHANNEL_ID is correct and the bot is an admin in the channel.")
            await update.message.reply_text(f"Error: Could not send to channel. Is the bot an admin?")
        
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred when sending to channel: {e}")
            await update.message.reply_text(f"An unexpected error occurred.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        The main handler for incoming text messages.
        """
        # Ignore updates that are not new messages (like edited messages)
        if not update.message:
            print("Ignoring non-message update (e.g., edited message)")
            return

        # Reloads config to get the latest values for this function
        if not await self.reload_config_on_the_fly():
            return # Error already printed by the reload function

        # --- Get latest values from the reloaded config ---
        user_id = update.message.from_user.id
        my_user_id = self.config.get('MY_USER_ID')
        channel_id = self.config.get('CHANNEL_ID')
        
        # --- User Validation ---
        if not my_user_id:
            # If MY_USER_ID is not set, print the user's ID so they can set it
            print(f"Received message from User ID: {user_id}. (Set MY_USER_ID to restrict access)")
            await update.message.reply_text(f"Set {user_id} in MY_USER_ID to restrict access")
            return

        if user_id != int(my_user_id):
            print(f"Unauthorized access attempt by User ID: {user_id}")
            await update.message.reply_text("This bot is private and only for the developer.")
            return
        
        # --- Process and Send Message ---
        user_text = update.message.text or ""
        html_text = telegram_format(user_text)

        # 1. Reply to the user
        await update.message.reply_text(html_text, parse_mode="HTML")
        
        # 2. Send to the channel (using the internal method)
        await self._send_to_channel(context, channel_id, html_text, update)

    def run(self):
        """
        Builds and runs the bot application.
        This is called after the initial __init__ validation.
        """
        app = ApplicationBuilder().token(self.bot_token).build()
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        print("Bot is running...")
        
        # Check the *initial* value of MY_USER_ID to print the helper message
        if not self.config.get('MY_USER_ID'):
            print("Send any message from the bot to receive your 'USER_ID'")
        
        app.run_polling()


if __name__ == "__main__":
    try:
        bot = TelegramBot()
        bot.run()
    
    except InvalidToken:
        exit_with_error(
            "Error: Invalid BOT_TOKEN.\n"
            "The token provided in 'config.json' was rejected by Telegram.\n"
            "Please get a new token from @BotFather and update your config file.",
            10
        )
    
    except Exception as e: # Catch any other unexpected startup errors
        exit_with_error(f"An unexpected startup error occurred: {e}", 10)

