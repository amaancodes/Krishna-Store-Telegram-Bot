import logging
import random
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Global variables to store products and orders
products = {'Apple': 1.5, 'Banana': 0.5, 'Orange': 1.0, 'Mango': 2.0}
orders = {}
affiliates = {}

def start(update, context):
    """Start the bot and display the available commands"""
    user = update.message.from_user
    update.message.reply_text(f"Hello {user.first_name}! I'm a grocery store bot. How can I assist you?"
                              "\n\nYou can use the following commands:"
                              "\n- /viewproducts: View available products"
                              "\n- /order: Place an order"
                              "\n- /vieworder: View your current order"
                              "\n- /becomeaffiliate: Become an affiliate")

def view_products(update, context):
    """Display the available products with their prices"""
    product_list = "Available products:\n"
    for product, price in products.items():
        product_list += f"{product} - ${price}\n"
    update.message.reply_text(product_list)

def order(update, context):
    """Start the ordering process and add quantity for each product"""
    user = update.message.from_user
    update.message.reply_text(f"{user.first_name}, please enter the products you want to order along with the quantity "
                              "(e.g., 'Apple 2', 'Banana 3'):")

def process_order(update, context):
    """Process the customer's order and calculate the total bill amount"""
    user = update.message.from_user
    order_items = update.message.text.split(',')

    if user.id not in orders:
        orders[user.id] = {}

    total_bill = 0.0

    for item in order_items:
        item = item.strip().split()
        if len(item) == 2:
            product_name = item[0]
            quantity = int(item[1])
            if product_name in products:
                price = products[product_name]
                total_price = price * quantity
                total_bill += total_price

                if product_name in orders[user.id]:
                    orders[user.id][product_name] += quantity
                else:
                    orders[user.id][product_name] = quantity
            else:
                update.message.reply_text(f"Sorry, '{product_name}' is not available.")

    update.message.reply_text(f"{user.first_name}, your order has been placed. "
                              f"Total bill amount: ${total_bill:.2f}")

def view_order(update, context):
    """Display the ordered items with the total bill amount"""
    user = update.message.from_user
    if user.id in orders:
        order_items = orders[user.id]
        if order_items:
            order_list = "Your order:\n"
            total_bill = 0.0
            for product_name, quantity in order_items.items():
                price = products[product_name]
                total_price = price * quantity
                order_list += f"{product_name} - {quantity} x ${price} = ${total_price:.2f}\n"
                total_bill += total_price

            order_list += f"Total bill amount: ${total_bill:.2f}"
            update.message.reply_text(order_list)
        else:
                        update.message.reply_text("You have not placed any orders yet.")
    else:
        update.message.reply_text("You have not placed any orders yet.")

def become_affiliate(update, context):
    """Generate a unique affiliate ID for users who want to become affiliates"""
    user = update.message.from_user
    affiliate_id = random.randint(1000, 9999)
    affiliates[user.id] = affiliate_id
    update.message.reply_text(f"{user.first_name}, congratulations! You have become an affiliate."
                              f"Your affiliate ID is: {affiliate_id}")

def main():
    """Start the bot"""
    # Set up the Telegram Bot token
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add handlers for commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("viewproducts", view_products))
    dp.add_handler(CommandHandler("order", order))
    dp.add_handler(CommandHandler("vieworder", view_order))
    dp.add_handler(CommandHandler("becomeaffiliate", become_affiliate))

    # Add handler for messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process_order))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()

