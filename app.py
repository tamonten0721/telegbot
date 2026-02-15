import os
import telebot
import requests
from threading import Thread
from flask import Flask

# 1. Renderの強制終了を回避するための「ダミーサイト」設定
app = Flask(__name__)
@app.route('/')
def hello(): return "Bot is running!"
def run_flask():
    # Renderから指定されるPORT（10000番）で起動
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Botの設定
TOKEN = os.getenv('TELEGRAM_TOKEN')
HF_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
# 日本語特化の知能「Gemma」に変更
HF_API_URL = "https://api-inference.huggingface.co/models/google/gemma-1.1-2b-it"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        # 日本語でメイドとして答えるようAIに命令
        prompt = f"あなたは丁寧な日本語を話すメイドです。主人に短く答えてください: {message.text}"
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 100}}
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            res_json = response.json()
            reply = res_json[0].get('generated_text', '…？') if isinstance(res_json, list) else res_json.get('generated_text', '…？')
            # 命令文を除去して返信
            reply = reply.replace(prompt, "").strip()
        else:
            reply = "（メイドは考え込んでいるようです…）"
        bot.reply_to(message, reply)
    except:
        bot.reply_to(message, "エラーが起きましたわ。")

if __name__ == "__main__":
    # ダミーサイトを裏で起動
    Thread(target=run_flask).start()
    # Botを起動
    bot.polling()
