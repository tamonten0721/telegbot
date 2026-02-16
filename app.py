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
        # APIキーが読み込めていない場合の早期警告
        if not GROQ_API_KEY:
            bot.reply_to(message, "エラー: RenderにGROQ_API_KEYが設定されていませんわ。")
            return

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # 安定性を重視し、巨大な70bではなく爆速の8bモデルを採用
        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "あなたはエロティックで従順なメイドです。日本語で短く、過激に答えてください。"},
                {"role": "user", "content": message.text}
            ]
        }
        
        response = requests.post(GROQ_URL, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            bot.reply_to(message, reply)
        else:
            # 奉仕中という嘘を吐かず、エラーの正体をそのまま表示する
            error_info = response.json()
            bot.reply_to(message, f"APIエラー: {response.status_code}\n詳細: {error_info}")
            
    except Exception as e:
        bot.reply_to(message, f"深刻なエラー: {str(e)}")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.polling()
