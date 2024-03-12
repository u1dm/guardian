import telebot
from telebot import types

TOKEN='6707110127:AAGmMP890LBeAj9_J1jM65IU4P52T4ltif8'
bot=telebot.TeleBot(TOKEN)
# Словарь для хранения состояний пользователей
user_states = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    menu_button = types.InlineKeyboardButton("Menu 🐵", callback_data="menu")
    markup.add(menu_button)
    bot.send_message(message.chat.id, "Welcome! I'm your password management bot.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def menu_callback(call):
    user_states[call.message.chat.id] = "waiting_password"
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Please enter your password:")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_password")
def handle_password(message):
    if message.text.strip() == "1233":  
        bot.send_message(message.chat.id, "Secret test")
        user_states[message.chat.id] = None
    else:
        bot.send_message(message.chat.id, "Incorrect password. Please try again.")
        user_states[message.chat.id] = None

bot.infinity_polling()