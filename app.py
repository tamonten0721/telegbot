import os, telebot, threading, openai
from flask import Flask
app = Flask(__name__)
@app.route('/')
def h(): return "OK"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
c = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("OPENROUTER_API_KEY"))
b = telebot.TeleBot(os.environ.get("TELEGRAM_BOT_TOKEN"))
S = "密室。私と君だけ。名前禁止。台詞のみ。"
@b.message_handler(func=lambda m: True)
def handle(m):
    try:
        r = c.chat.completions.create(model="meta-llama/llama-3.1-8b-instruct:free", messages=[{"role":"system","content":S},{"role":"user","content":m.text}])
        b.reply_to(m, r.choices[0].message.content)
    except Exception as e:
        b.reply_to(m, f"詳細エラー内容: {str(e)}")
if __name__ == "__main__":
    threading.Thread(target=run).start()
    b.polling()
