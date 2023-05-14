import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# States of the conversation
SELECTING_OPTION, ADDING_ITEMS, TAKING_ORDER = range(3)

# Helper function to start the bot
def start(update: Update, _: CallbackContext) -> int:
    reply_keyboard = [['View Inventory', 'Take Order']]

    update.message.reply_text(
        'Welcome to the Grocery Store Bot!\n\n'
        'What would you like to do?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return SELECTING_OPTION

# Function to handle the "View Inventory" command
def view_inventory(update: Update, _: CallbackContext) -> int:
    # Replace with your logic to fetch and display the inventory
    inventory = get_inventory()  # Function to fetch the inventory

    update.message.reply_text(
        f'Current Inventory:\n\n{inventory}',
        reply_markup=ReplyKeyboardRemove(),
    )

    return SELECTING_OPTION

# Function to handle the "Take Order" command
def take_order(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        'Please enter the items you want to order, separated by commas:',
        reply_markup=ReplyKeyboardRemove(),
    )

    return TAKING_ORDER

# Function to handle the user's order
def process_order(update: Update, _: CallbackContext) -> int:
    order = update.message.text

    # Replace with your logic to process the order
    process_order(order)  # Function to process the order

    update.message.reply_text('Your order has been placed. Thank you!')

    return SELECTING_OPTION

# Function to handle unknown commands
def unknown(update: Update, _: CallbackContext) -> int:
    update.message.reply_text('Sorry, I didn\'t understand that command.')

    return SELECTING_OPTION

# Function to handle errors
def error(update: Update, context: CallbackContext) -> None:
    logger.error(f'Update "{update}" caused error "{context.error}"')

# Function to stop the bot
def stop(update: Update, _: CallbackContext) -> int:
    update.message.reply_text('Goodbye!')

    return ConversationHandler.END

def get_inventory():
    # Replace with your actual logic to fetch the inventory
    # This is just a sample implementation

    # Sample inventory data
    inventory = {
        'apple': 10,
        'banana': 15,
        'orange': 20,
        'grape': 8,
        'mango': 12
    }

    # Generate a formatted string for displaying the inventory
    inventory_str = '\n'.join([f'{item}: {quantity}' for item, quantity in inventory.items()])

    return inventory_str

def process_order(order):
    # Replace with your actual logic to process the order
    # This is just a sample implementation

    # Split the order string into individual items
    items = [item.strip() for item in order.split(',')]

    # Process each item in the order
    for item in items:
        # Replace with your logic to update the inventory or perform any other necessary operations
        # Here, we are just printing the item as a placeholder
        print(f"Processing item: {item}")

    # You can also save the order details to a database or perform any other necessary actions

    # This is just a sample implementation to show that the order has been processed
    print("Order processed successfully")


def main() -> None:
    # Set up the bot
    updater = Updater('YOUR_BOT_TOKEN')
    dispatcher = updater.dispatcher

    # Define conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_OPTION: [
                MessageHandler(Filters.regex('^View Inventory$'), view_inventory),
                MessageHandler(Filters.regex('^Take Order$'), take_order),
            ],
            TAKING_ORDER: [MessageHandler(Filters.text, process_order)],
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    # Add conversation handler to the dispatcher
    dispatcher.add_handler(conv_handler)

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
