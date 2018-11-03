from flask import Flask, request, render_template
from urllib.request import Request, urlopen
import json

app = Flask(__name__)

BOT_BEARER = "ODc2YTBkN2MtNjlhYy00YmI1LWFiMjEtYWY3ZjZjZGViZTE3MmEzNDc5M2ItZTIx"
SPARK_MESSAGES_URL = "https://api.ciscospark.com/v1/messages/"
BOT_EMAIL = "codevis@webex.bot"
BOT_NAME = "codevis"

def sendGetRequest(url):
    my_headers = {"Accept" : "application/json", "Content-Type" : "application/json"}
    request = Request(url, headers=my_headers)
    request.add_header("Authorization", "Bearer " + BOT_BEARER)
    contents = urlopen(request).read()
    return contents

def sendPostRequest(url, data):
    my_headers = {"Accept" : "application/json", "Content-Type" : "application/json"}
    request = Request(url, data=json.dumps(data).encode('utf-8'), headers=my_headers)
    request.add_header("Authorization", "Bearer " + BOT_BEARER)
    contents = urlopen(request).read()
    return contents

@app.route("/", methods=["POST"])
def index():
    webhook = json.loads(request.data)
    # print("############################################################")
    # print("REQUEST.data: {0}".format(request.data))
    # print("REQUEST: {0}".format(request))
    # print("ARGS: {0}".format(request.args))
    # print("FORM: {0}".format(request.form))
    # print("FILES: {0}".format(request.files))
    # print("VALUES: {0}".format(request.values))
    # print("############################################################")
    if webhook['data']['personEmail'] != BOT_EMAIL:
        print("[APP] {0}".format(webhook['data']['id']))
        result = sendGetRequest(SPARK_MESSAGES_URL + webhook['data']['id'])
        result = json.loads(result)
        in_message = result.get('text', '').lower()
        print("[APP] in_message: {0}".format(in_message))
        sendPostRequest("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "This is a test image", "files":["https://i.redd.it/ho7von2212w11.jpg"})
        #sendPostRequest("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": in_message})
    return "true"

if __name__ == "__main__":
    app.run()
# run_itty(server='wsgiref', host='127.0.0.1', port=4040)
