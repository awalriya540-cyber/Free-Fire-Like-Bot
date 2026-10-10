import os
import telebot
import requests

# আপনার টেলিগ্রাম বটের টোকেন এবং আইডি নম্বর
BOT_TOKEN = "8941740632:AAGluj-QR0NjrBn2k5z-mlq8R8uwdnWTnko"
OWNER_ID = 8804023988

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 স্বাগতম! ফ্রি ফায়ার অটো-লাইক বটে।\n\n"
        "লাইক নিতে নিচের নিয়মে মেসেজ দিন:\n"
        "`/like <Region> <UID>`\n\n"
        "উদাহরণ: `/like BD 13272570211`"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['like'])
def send_likes(message):
    # মালিক ভেরিফিকেশন চেক
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ আপনি এই বটের মালিক নন!")
        return

    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "⚠️ সঠিক নিয়ম: `/like <Region> <UID>`\nউদাহরণ: `/like BD 13272570211`")
            return
            
        region = args[1].upper() # ১ম পজিশন থেকে রিজিয়ন নেওয়া (BD)
        uid = args[2]            # ২য় পজিশন থেকে ইউআইডি নেওয়া
        
        bot.reply_to(message, f"⏳ আপনার ইউআইডি ({uid})-এ লাইক পাঠানো শুরু হয়েছে... অনুগ্রহ করে ১-২ মিনিট গেমের ভেতরে চেক করুন।")
        
        # পাবলিক ফ্রি লাইক এপিআই রিকোয়েস্ট
        public_api_url = f"https://railway.app{region}&uid={uid}"
        response = requests.get(public_api_url, timeout=15)
        
        if response.status_code == 200:
            bot.send_message(message.chat.id, f"✅ সফলভাবে ইউআইডি: {uid}-এ লাইক পাঠানো সম্পন্ন হয়েছে!")
        else:
            bot.send_message(message.chat.id, "❌ এই মুহূর্তের ফ্রি সার্ভারটি ফুল আছে। দয়া করে কিছুক্ষণ পর আবার চেষ্টা করুন।")
            
    except Exception as e:
        bot.send_message(message.chat.id, "⏳ সার্ভার প্রসেসিং চলছে, দয়া করে আপনার গেমের প্রোফাইলটি চেক করে দেখুন।")

if __name__ == "__main__":
    bot.infinity_polling()
