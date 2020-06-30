import os
from flask import Flask, request, abort
from flask.logging import create_logger 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
LOG = create_logger(app)

line_bot_api = LineBotApi('hCXvdsA1ZbuV3qdFCu2ctdEBgUEF4iVzH6eJ7g3ptXxvXJMRd1jrTzqj3pBumTFzMJNgHK1T21nK7s3Mvy+VboMpODA9uC5LzvqdqzjmtXZHWGpP3NTVqjxVFBH6InLxr7amogyZtQzWHT7LqIrUyQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('93b85ca6314b6ab97cd5f0ec5bc73436')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    LOG.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    msg = (event.message.text).lower()

    if ('hai' in msg) or ('hello' in msg) or ('hai' in msg) or ('hi' in msg) :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hello pengguna!'))
    else :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
