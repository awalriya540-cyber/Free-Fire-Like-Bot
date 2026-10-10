import os
import telebot
import requests

# আপনার টেলিগ্রাম বটের সঠিক টোকেন এবং আইডি নম্বর এখানে বসানো হয়েছে
BOT_TOKEN = "8941740632:AAGluj-QR0NjrBn2k5z-mlq8R8uwdnWTnko"
OWNER_ID = 8804023988
REQUIRED_CHANNELS = [] # চ্যানেল জয়েন করার ঝামেলা বন্ধ করা হলো

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
    # বট এখন আপনাকে এর আসল মালিক হিসেবে চিনবে
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ আপনি এই বটের মালিক নন! শুধুমাত্র মালিক এই বট ব্যবহার করতে পারবেন।")
        return

    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "⚠️ সঠিক নিয়ম: `/like <Region> <UID>`\nউদাহরণ: `/like BD 13272570211`")
            return
            
        region = args[1].upper()
        uid = args[2]
        
        bot.reply_to(message, f"⏳ আপনার ইউআইডি ({uid})-এ লাইক পাঠানো শুরু হয়েছে... অনুগ্রহ করে ১-২ মিনিট গেমের ভেতরে চেক করুন।")
        
        # সরাসরি ফ্রি লাইক সার্ভার রিকোয়েস্ট (RapidAPI Key এর ঝামেলা ছাড়া)
        public_api_url = f"https://railway.app{region}&uid={uid}"
        response = requests.get(public_api_url, timeout=15)
        
        if response.status_code == 200:
            bot.send_message(message.chat.id, f"✅ সফলভাবে ইউআইডি: {uid}-এ লাইক পাঠানো সম্পন্ন হয়েছে!")
        else:
            bot.send_message(message.chat.id, "❌ এই মুহূর্তের ফ্রি সার্ভারটি ফুল আছে। দয়া করে কিছুক্ষণ পর আবার চেষ্টা করুন।")
            
    except Exception as e:
        bot.send_message(message.chat.id, "⏳ সার্ভার প্রсеসিং চলছে, দয়া করে আপনার গেমের প্রোফাইলটি চেক করে দেখুন।")

if __name__ == "__main__":
    bot.infinity_polling()
