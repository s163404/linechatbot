# インポートするライブラリ
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os
import datetime

# 軽量なアプリケーションフレームワーク：Flask
app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
# 環境変数からアクセストークンを設定
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
# line_bot_api = LineBotApi('Tn4s4pPIU4UgRVP19wXHLT8xUbDgmpwzeWT4ReE/GMdTTj9NC2zCg2YCJomZ8yKV1NaVXooE1G883dbUziEYPv60bofHHnflyGT7kEspt7bfxo3EBUrg2w4hJL6rhTOuaYRJwDNGO8UAfZWiko4D4AdB04t89/1O/w1cDnyilFU=')
# 環境変数からチャンネルシークレットを設定
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
# handler = WebhookHandler('e85520b00d4e6f0ca9b37524dd0670a2')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    # あいさつリプライ
    # 拾うあいさつ集を作って辞書化する ->後日実装
    if text == "おはよう" or text == "こんにちは" or text == "こんばんは":
        hour_now = datetime.datetime.now().hour + 9 
        reply_text = 'おは！' if hour_now >= 4 and hour_now <= 10 else 'お昼食べた？' if hour_now >= 11 and hour_now <= 16 else 'こんばんは'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text))
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
