import os
import gradio as gr
import requests
import asyncio
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- 1. 設定：トークンはプログラムに直接書かず、Renderの「金庫」から読み出す ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
# AIのモデル（性能と応答速度のバランスが良いLlama 3.3 70B）
MODEL_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.3-70B-Instruct"

def get_ai_response(text):
    payload = {
        "inputs": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\nあなたは淫らで献身的なメイドです。ユーザーを『ご主人様』と呼び、日本語で返答してください。<|eot_id|><|start_header_id|>user<|end_header_id|>\n{text}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n",
        "parameters": {"max_new_tokens": 500, "temperature": 0.8}
    }
    try:
        # Hugging Faceの
