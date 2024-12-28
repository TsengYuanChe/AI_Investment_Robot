from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from CH6 import stock_gpt, get_reply

app = Flask(__name__)

# 配置 LINE Messaging API 憑證
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/webhook", methods=['POST'])
def webhook():
    # 獲取 X-Line-Signature 標頭
    signature = request.headers['X-Line-Signature']

    # 獲取請求 body
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 檢測是否為4位數的股票代碼或「大盤」訊息
    if (len(user_message) == 4 and user_message.isdigit()) or user_message == '大盤':
        reply_text = stock_gpt(user_message)
    # 一般訊息
    else:
        msg = [  {"role": "system",
                  "content":"reply in 繁體中文"
              }, {"role": "user",
                  "content":user_message}]
        reply_text = get_reply(msg)
      
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)