import os
import telebot
import requests

# 環境変数からトークンを取得
TOKEN = os.getenv('TELEGRAM_TOKEN')
HF_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # Hugging FaceのAPIを叩く
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {"inputs": message.text}
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        
        if response.status_status == 200:
            reply = response.json().get('generated_text', '…？')
        else:
            reply = "（メイドは考え込んでいるようです…）"
            
        bot.reply_to(message, reply)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "エラーが起きましたわ。")

if __name__ == "__main__":
    bot.polling()
