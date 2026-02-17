import os
import telebot
from google.generativeai import GenerativeModel
import google.generativeai as genai

# 1. 初期設定
token = os.environ['TELEGRAM_TOKEN']
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
bot = telebot.TeleBot(token)
model = GenerativeModel("gemini-1.5-flash")

# 2. 稼ぎのロジック（システムプロンプト）
S = """あなたは『負け組脱出』に特化した、最強の現金生成AIだ。
ユーザーは任意整理中のため、信用情報が必要な案件は100%排除せよ。
以下の3カテゴリの情報を、ネットから24時間監視・抽出せよ。

①【即金】審査なし・高単価セルフバック（不動産査定、公共インフラ切替、口座開設等）。
②【0円エアドロ】SNSタスク（フォロー・投稿）だけで完結するリスクゼロ案件。
③【勝負エアドロ】期待値$500以上。ガス代（数百円）を払う価値がある厳選案件。

報告形式：
【ジャンル】
【案件名】
【期待収益】円/USDで具体的に
【手順】リテラシー不問の3ステップ
【次のリスク】この案件の懸念点を1つ

※形容詞を禁止し、全て数値と事実で語れ。論理的欠陥は容赦なく指摘しろ。"""

# 3. 起動メッセージ
def start_hunting():
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    response = model.generate_content(S + "\n今すぐ稼げる最新情報を3つ抽出して報告せよ。")
    bot.send_message(chat_id, response.text)

if __name__ == "__main__":
    start_hunting()
