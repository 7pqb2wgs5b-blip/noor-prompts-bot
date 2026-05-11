import os
import requests
import telebot

TELEGRAM_TOKEN = os.environ.get(“TELEGRAM_TOKEN”)
GEMINI_API_KEY = os.environ.get(“GEMINI_API_KEY”)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def generate_prompt(user_idea):
url = f”https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}”

```
system_text = """You are an expert AI image prompt engineer. 
The user will give you a simple idea in Arabic or English.
Generate a professional, detailed image prompt in English suitable for Midjourney, DALL-E, and Ideogram.
Format your response as:

🎨 **Midjourney:**
[prompt] --ar 16:9 --q 2 --v 6

🖼️ **DALL-E:**
[prompt]

✨ **Ideogram:**
[prompt]

Make the prompts vivid, detailed, and professional."""

payload = {
    "contents": [{
        "parts": [{
            "text": f"{system_text}\n\nUser idea: {user_idea}"
        }]
    }]
}

response = requests.post(url, json=payload)
data = response.json()

try:
    return data["candidates"][0]["content"]["parts"][0]["text"]
except:
    return "❌ حدث خطأ، حاول مرة أخرى"
```

@bot.message_handler(commands=[“start”])
def start(message):
bot.reply_to(message, “”“👋 أهلاً بك في NoorPrompts Bot!

🤖 أنا بحول أفكارك البسيطة لبرومبتات احترافية للذكاء الاصطناعي

✅ يدعم: Midjourney | DALL-E | Ideogram

📝 ببساطة أرسل لي فكرتك بالعربي أو الإنجليزي وأنا أولّد لك البرومبت!

مثال: “صورة غروب شمس على البحر مع قارب خشبي” “””)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
user_idea = message.text
bot.reply_to(message, “⏳ جاري توليد البرومبت…”)

```
result = generate_prompt(user_idea)
bot.reply_to(message, result, parse_mode="Markdown")
```

if **name** == “**main**”:
print(“✅ NoorPrompts Bot is running…”)
bot.polling(none_stop=True)