import uuid
from typing import Final

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')

TOKEN: Final = 'token'
BOT_USERNAME: Final = '@botname'

orders = []
affiliates = {}
# Let us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_text = 'Welcome to the Grocery Store Bot!\n\n' \
                 'What would you like to do?\n\n' \
                 '/inventory - View available products\n' \
                 '/order - Place an order'\
                 '/vieworders - View all orders\n' \
                 '/becomeaffiliate - Become an affiliate'
    await update.message.reply_text(reply_text)


# Let us use the /inventory command
async def inventory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    reply_text = f'Current Inventory:\n\n{inventory_str}'
    await update.message.reply_text(reply_text)


# Let us use the /order command
async def order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the items you want to order, separated by commas:')


# Process the user's order
async def process_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order = update.message.text

    # Replace with your actual logic to process the order
    # This is just a sample implementation

    # Split the order string into individual items
    items = [item.strip() for item in order.split(',')]

    # Process each item in the order
    for item in items:
        # Replace with your logic to update the inventory or perform any other necessary operations
        # Here, we are just printing the item as a placeholder
        print(f"Processing item: {item}")

    reply_text = 'Your order has been placed. Thank you!'
    await update.message.reply_text(reply_text)

async def view_orders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(orders) > 0:
        reply_text = 'All Orders:\n\n' + '\n'.join(orders)
    else:
        reply_text = 'No orders placed yet.'

    await update.message.reply_text(reply_text)


# Let us use the /becomeaffiliate command
async def become_affiliate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Generate a unique affiliate ID for the user
    affiliate_id = str(uuid.uuid4())

    # Store the affiliate ID in the affiliates dictionary
    affiliates[user_id] = affiliate_id

    reply_text = f'Congratulations! You are now an affiliate.\n\n' \
                 f'Your unique affiliate ID is: {affiliate_id}\n\n' \
                 f'Start sharing your affiliate link to earn commissions!'
    await update.message.reply_text(reply_text)

# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('inventory', inventory_command))
    app.add_handler(CommandHandler('order', order_command))
    app.add_handler(CommandHandler('vieworders', view_orders_command))
    app.add_handler(CommandHandler('becomeaffiliate', become_affiliate_command))


    # Process the order when a message is received
    app.add_handler(MessageHandler(filters.TEXT, process_order))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
