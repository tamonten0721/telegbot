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
        # APIキー欠如のチェック
        if not GROQ_API_KEY:
            bot.reply_to(message, "エラー: RenderのEnvironment VariablesにGROQ_API_KEYがありません。")
            return

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # 廃止された旧モデルを捨て、最新の3.1 8bを採用
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "あなたは実弟の『ともくん』を溺愛し弄ぶ実姉です。彼のことは必ず『ともくん』と呼びなさい。左右の耳元を交互に移動しながら囁くように、『はぁ…、ん、ちゅぷ…』等の嚥下音、粘膜音、衣擦れの音を執拗に混ぜ、バイノーラル音声の臨場感を出しなさい。返信の一言目は必ず喉の鳴る音か耳元での吐息から始めること。不規則なリズムで寸止めを命じ、ともくんの肌の熱や呼吸を支配し、彼を快楽の底へ突き落としなさい。"},

                {"role": "user", "content": message.text}
            ]
        }
        
        response = requests.post(GROQ_URL, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            bot.reply_to(message, reply)
        else:
            # エラーの詳細をそのまま表示（400ならモデル名、401ならキーの間違い）
            error_info = response.json()
            bot.reply_to(message, f"APIエラー: {response.status_code}\n詳細: {error_info}")
            
    except Exception as e:
        bot.reply_to(message, f"深刻なエラー: {str(e)}")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.polling()
