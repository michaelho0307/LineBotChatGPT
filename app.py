from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
import os
import openai
app = Flask(__name__)
load_dotenv()
# set Line Bot's Channel Access Token and Channel Secret
#api_key = os.environ.get("API_KEY")
line_bot_api = LineBotApi(os.environ.get("CHANNELACCESSTOKEN"))
handler = WebhookHandler(os.environ.get("CHANNELSECRET"))
openai.api_key=os.environ.get("CHATGPTAPIKEY")

# define Webhook route
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# define message handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        #print(event.message.text)
        if (len(event.message.text)<10):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Please enter more than ten words."))
        else:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=event.message.text,
                max_tokens=2500, #maybe larger
                #n=1,
                #stop=None,
                temperature=0.3,
            )
            # reply msg
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response["choices"][0]["text"].strip()))
    except LineBotApiError as e:
        print(e)

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text)
    # )

def main():
    app.run()
#if __name__ == "__main__":
    #app.run()
    #app.run(host='0.0.0.0', port=8080)
#app = Flask(__name__)