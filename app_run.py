from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from testsearchforwin import searchall
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)
CORS(app, resources=r'/*')

line_bot_api = LineBotApi('lPZrWaAs+laA1syJBXiHWRggMCp3ycjzBVDjvdL2coi/iOYivCqO3cBD+n0nmmlylAh995ATKmcTOo3hxOGuYe1EQWiJ4WUcG1PR91X2hfNvOCF/42UW+JHe1Ls0CKVlFKuAu8i0AxQG4qaLcImg5wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d153cf07677f8f14f7aeed20ee3aa39b')


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    a = searchall(event.message.text) 

    if(a[0]!=0):
        line_bot_api.reply_message(
            event.reply_token,[
            #TextSendMessage(text=event.message.text),
            TextSendMessage(text="危險指數：" + a[3] + "%"),
            TextSendMessage(text="公司資訊："+a[2]+"\n最後更新："+a[0]+"\n到期日期："+a[1]),
            ]
        )
    
    else:
        line_bot_api.reply_message(
            event.reply_token,[
            TextSendMessage(text=event.message.text),
            TextSendMessage(text="無法得知公司資訊")
            ]
        )


if __name__ == "__main__":
    app.run()
