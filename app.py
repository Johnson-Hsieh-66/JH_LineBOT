import os
from flask import Flask, request, abort
from linebot.v3 import (WebhookHandler)
from linebot.v3.exceptions import (InvalidSignatureError)
from linebot.v3.messaging import (Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage)
from linebot.v3.webhooks import (MessageEvent, TextMessageContent)
from linebot.v3.messaging.models.push_message_request import PushMessageRequest
from linebot.v3.messaging.models.push_message_response import PushMessageResponse
from linebot.v3.messaging.rest import ApiException
from pprint import pprint
from lib import handleFunction

app = Flask(__name__)

configuration = Configuration(access_token=os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))
strUserId = os.environ.get('LineUserId')


@app.route("/pushMessage/getCrudeOil")
def getCrudeOil():
    content = handleFunction.getOilPrice()
    push_message(content)
    return content


@app.route("/pushMessage/getStockInfos")
def getStockInfos():
    listStock = ['2330', '2317']
    content = handleFunction.getStockInfos(listStock)
    push_message(content)
    return content


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


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    content = event.message.text
    if event.message.text == "@PTT":
        content = 'PTT'
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=content)]
            )
        )


def push_message(content):
    # Enter a context with an instance of the API client
    with ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = MessagingApi(api_client)
        push_message_request = PushMessageRequest(to=strUserId, messages=[TextMessage(text=content)])
        try:
            api_response = api_instance.push_message(push_message_request)
            print("The response of MessagingApi->push_message:\n")
            #pprint(api_response)
        except Exception as e:
            print("Exception when calling MessagingApi->push_message: %s\n" % e)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
