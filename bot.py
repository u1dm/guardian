import telebot
from telebot import types

TOKEN='6707110127:AAGmMP890LBeAj9_J1jM65IU4P52T4ltif8'
bot=telebot.TeleBot(TOKEN)

user_passwords = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    menu_button = types.InlineKeyboardButton("Menu 🐵", callback_data="menu")
    markup.add(menu_button)
    bot.send_message(message.chat.id, "Welcome! I'm your password management bot.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def menu_callback(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('My passwords 📂')
    itembtn2 = types.KeyboardButton('Lock 🔒')
    markup.add(itembtn1, itembtn2)
    bot.send_message(call.message.chat.id, "You are in the main menu, select an action 🔽", reply_markup=markup)
@bot.message_handler(func=lambda message: True)

def echo_all(message):
    if message.text == "My passwords 📂":
        user_id = message.from_user.id
        if user_id in user_passwords:
            passwords = user_passwords[user_id]
            passwords_text = "Your passwords 📄:\n"
            for login, password in passwords:
                passwords_text += f"- Login: {login}, Password: {password}\n"
        else:
            passwords_text = "You haven't added any passwords yet 🙊"
        
        markup = types.InlineKeyboardMarkup()
        add_button = types.InlineKeyboardButton("Add 🔑", callback_data="add")
        remove_button = types.InlineKeyboardButton("Remove 🗑", callback_data="remove")
        markup.add(add_button, remove_button)
        
        bot.reply_to(message, passwords_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "add")
def add_password_callback(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Please enter the login 🙈")
    bot.register_next_step_handler(call.message, process_login_step)

def process_login_step(message):
    user_id = message.from_user.id
    login = message.text
    bot.send_message(message.chat.id, "Please enter the password 🙈")
    bot.register_next_step_handler(message, lambda msg: process_password_step(msg, login))

def process_password_step(message, login):
    user_id = message.from_user.id
    password = message.text
    if user_id not in user_passwords:
        user_passwords[user_id] = []
    user_passwords[user_id].append((login, password))
    bot.send_message(message.chat.id, "Login and password added successfully 🙉")

bot.infinity_polling()