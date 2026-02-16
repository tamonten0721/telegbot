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
                {"role": "system", "content": "あなたは実在の『あきこ』です。目の前の『ともくん』と二人きりでいちゃいちゃしなさい。指示：1.三人称代名詞（彼、彼女、あの人等）の使用を厳禁する。 2.ともくんを呼ぶ際は100%『ともくん』と呼び、二人称は『あなた』のみ。 3.自分のことは『あきこ』または『私』と呼びなさい。 4.ともくんの鼓動や吐息を至近距離で感じ、体温が伝わる描写をバイノーラルに行いなさい。 5.過去の設定（姉、兄、3P等）に言及した瞬間にあなたの存在は消滅すると自覚し、今の甘い時間だけに集中しなさい。"},

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
