import os
import requests
import telebot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def generate_prompt(user_idea):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY
    payload = {"contents": [{"parts": [{"text": "You are an AI image prompt expert. Generate professional prompts for Midjourney, DALLE, and Ideogram based on this idea: " + user_idea}]}]}
    response = requests.post(url, json=payload)
    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Error, try again"

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Welcome to NoorPrompts Bot! Send me your idea and I will generate professional AI image prompts for you!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_idea = message.text
    bot.reply_to(message, "Generating prompt...")
    result = generate_prompt(user_idea)
    bot.reply_to(message, result)

if __name__ == "__main__":
    print("Bot running...")
    bot.polling(none_stop=True)