from flask import Flask, request, abort
from linebot.v3 import (WebhookHandler)
from linebot.v3.exceptions import (InvalidSignatureError)
from linebot.v3.messaging import (MessagingApi, ReplyMessageRequest, TextMessage)
from linebot.v3.webhooks import (MessageEvent, TextMessageContent)
import os

app = Flask(__name__)

handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))
line_bot_api = MessagingApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))


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
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextMessage(text=event.message.text))
    # line_bot_api.reply_message(
    #     ReplyMessageRequest(
    #         reply_token=event.reply_token,
    #         messages=[TextMessage(text=event.message.text)]
    #     )
    # )


if __name__ == "__main__":
    app.run()
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
