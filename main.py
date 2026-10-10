
import os
import telebot
from telebot import types
import requests

# একদম শুরুর কোড (আপনার টোকেন ও আইডি সহ)
BOT_TOKEN = "8941740632:AAGluj-QR0NjrBn2k5z-mlq8R8uwdnWTnko"
REQUIRED_CHANNELS = [] 
OWNER_ID = 8804023988
OWNER_USERNAME = "@awalriya"

bot = telebot.TeleBot(BOT_TOKEN)

def is_user_joined(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not is_user_joined(user_id):
        markup = types.InlineKeyboardMarkup()
        for channel in REQUIRED_CHANNELS:
            markup.add(types.InlineKeyboardButton(text=f"Join Channel", url=f"https://t.me{channel[1:]}"))
        markup.add(types.InlineKeyboardButton(text="Verified ✅", callback_data="check_join"))
        bot.reply_to(message, "You must join our channels to use this bot:", reply_markup=markup)
    else:
        bot.reply_to(message, "You're verified! Welcome to the Free Fire Like Bot.\nUse `/like <region> <uid>` to get likes.")

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join_callback(call):
    user_id = call.from_user.id
    if is_user_joined(user_id):
        bot.answer_callback_query(call.id, "Verification successful! 🎉")
        bot.edit_message_text("You're verified! Welcome to the Free Fire Like Bot.\nUse `/like <region> <uid>` to get likes.", chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "You haven't joined all channels yet! ❌", show_alert=True)

@bot.message_handler(commands=['like'])
def send_like(message):
    user_id = message.from_user.id
    if not is_user_joined(user_id):
        bot.reply_to(message, "Please join the channels first by typing /start.")
        return

    command_parts = message.text.split()
    if len(command_parts) != 3:
        bot.reply_to(message, "Invalid format! Use: `/like <region> <uid>`\nExample: `/like bd 123456789`")
        return

    region = command_parts[1].lower()
    uid = command_parts[2]

    bot.reply_to(message, f"Sending likes to UID: {uid} in region: {region.upper()}... Please wait.")

    api_url = f"https://railway.app{region}&uid={uid}"
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            bot.send_message(message.chat.id, f"Successfully sent likes to UID: {uid}! ✅")
        else:
            bot.send_message(message.chat.id, "API Error: API Failed")
    except Exception:
        bot.send_message(message.chat.id, "API Error: API Failed")

if __name__ == '__main__':
    bot.polling(none_stop=True)
