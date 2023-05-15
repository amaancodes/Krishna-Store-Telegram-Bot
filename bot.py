import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to store product data and user orders
products = {
    'Wheat': '50/kg',
    'Rice': '30/kg',
    'Oil': '120/kg',
    'Bread': '25/loaf',
    'Milk': '50/litre',
    'Eggs': '6/piece',
    'Bread': '25/loaf',
    'Sugar': '30/kg',
    'ParleG': '10/piece',
    'Nirma': '52/kg',
    'Salt': '20/kg',
    'Tea': '110/kg'
}
orders = {}
affiliates = {}

# Start command
def start(update, context):
    update.message.reply_text(
        "Welcome to the grocery store bot!\n"
        "You can use the following commands:\n"
        "/viewproducts - View available products\n"
        "/order - Place an order\n"
        "/vieworder - View your order\n"
        "/becomeaffiliate - Become an affiliate\n"
        "/exit - Exit the bot"
    )

# View products command
def view_products(update, context):
    products_list = "\n".join([f"{product} - Rs{price}" for product, price in products.items()])
    update.message.reply_text(f"Available products:\n{products_list}")

# Order conversation
def order_start(update, context):
    update.message.reply_text("Please enter the product name and quantity (e.g., Apple 5). "
                              "Type /done to finish ordering.")
    return "ordering"

def order(update, context):
    message = update.message.text.strip().split()
    if len(message) != 2:
        update.message.reply_text("Invalid format. Please enter the product name and quantity.")
        return "ordering"
    
    product_name = message[0]
    quantity = int(message[1])
    
    if product_name not in products:
        update.message.reply_text("Invalid product name. Please try again.")
        return "ordering"
    
    if quantity <= 0:
        update.message.reply_text("Invalid quantity. Please enter a positive value.")
        return "ordering"
    
    if update.message.from_user.id not in orders:
        orders[update.message.from_user.id] = {}
    
    orders[update.message.from_user.id][product_name] = quantity
    update.message.reply_text("Product added to your order.")
    
    return "ordering"

def order_done(update, context):
    total_amount = 0
    order_details = ""

    if update.message.from_user.id in orders:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.username
        for product_name, quantity in orders[user_id].items():
            price = products[product_name]
            amount = price * quantity
            total_amount += amount
            order_details += f"{product_name} x{quantity} - Rs{amount}\n"

        if order_details:
            order_details += f"\nTotal amount: Rs{total_amount}"
            update.message.reply_text(f"Order details:\n{order_details}\n\nThank you for your order!")

            # Send order details to the user
            context.bot.send_message(
                chat_id=user_id,
                text=f"Order details:\n{order_details}\n\nThank you for your order, {user_name}!"
            )
        else:
            update.message.reply_text("Your order is empty.")
    else:
        update.message.reply_text("Your order is empty.")

    return ConversationHandler.END

def view_order(update, context):
    if update.message.from_user.id in orders:
        order_details = ""
        total_amount = 0

        for product_name, quantity in orders[update.message.from_user.id].items():
            price = products[product_name]
            amount = price * quantity
            total_amount += amount
            order_details += f"{product_name} x{quantity} - Rs{amount}\n"

        if order_details:
            order_details += f"\nTotal amount: Rs{total_amount}"
            update.message.reply_text(f"Your order:\n{order_details}")
        else:
            update.message.reply_text("Your order is empty.")
    else:
        update.message.reply_text("Your order is empty.")

# Become affiliate command
def become_affiliate(update, context):
    user_id = update.message.from_user.id
    if user_id not in affiliates:
        affiliate_id = len(affiliates) + 1
        affiliates[user_id] = affiliate_id
        update.message.reply_text(f"You are now an affiliate. Your affiliate ID is {affiliate_id}.")
    else:
        update.message.reply_text("You are already an affiliate.")

# Exit command
def exit_bot(update, context):
    update.message.reply_text("Thank you for using the grocery store bot. Have a great day!")
    return ConversationHandler.END

def main():
    # Create the Updater and Dispatcher
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dispatcher = updater.dispatcher

    # Add conversation handler for the order flow
    order_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("order", order_start)],
        states={
            "ordering": [MessageHandler(Filters.text & ~Filters.command, order)],
        },
        fallbacks=[CommandHandler("done", order_done)],
    )
    dispatcher.add_handler(order_conv_handler)

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("viewproducts", view_products))
    dispatcher.add_handler(CommandHandler("vieworder", view_order))
    dispatcher.add_handler(CommandHandler("becomeaffiliate", become_affiliate))
    dispatcher.add_handler(CommandHandler("exit", exit_bot))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
