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
    request = Request(url, json.dumps(data), headers=my_headers)
    request.add_headers("Authorization", "Bearer " + BOT_BEARER)
    contents = urlopen(request).read()
    return contents

@app.route("/", methods=["POST"])
def index(request):
    webhook = json.loads(request.body)
    print(webhook['data']['id'])
    result = sendGetRequest(SPARK_MESSAGES_URL + webhook['data']['id'])
    result = json.loads(result)
    in_message = result.get('text', '').lower()
    sendPostRequest("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": in_message})
    return "true"

if __name__ == "__main__":
    app.run(debug=True, port=4040)
# run_itty(server='wsgiref', host='127.0.0.1', port=4040)
