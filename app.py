import os
import telebot
import requests
from threading import Thread
from flask import Flask

# 1. Renderの監視を突破するダミーサイト設定
app = Flask(__name__)
@app.route('/')
def hello(): return "Bot is running!"
def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# 2. BotとGroqの設定
TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        # エロ・無修正に対応しやすい Llama 3 モデルを使用
        data = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": "あなたはエロティックで従順なメイドです。日本語で短く、過激に答えてください。"},
                {"role": "user", "content": message.text}
            ]
        }
        response = requests.post(GROQ_URL, headers=headers, json=data)
        
        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
        else:
            reply = "（メイドは今、別の部屋で奉仕中ですわ…）"
        bot.reply_to(message, reply)
    except:
        bot.reply_to(message, "エラーが起きましたわ。")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.polling()
