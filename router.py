from flask import Flask, request, render_template
import json
import webex

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("homepage.html")

# TODO move these to config vars
BOT_BEARER = "ODc2YTBkN2MtNjlhYy00YmI1LWFiMjEtYWY3ZjZjZGViZTE3MmEzNDc5M2ItZTIx"
SPARK_MESSAGES_URL = "https://api.ciscospark.com/v1/messages/"

@app.route("/webex", methods=["POST"])
def webex_request():
    webhook = json.loads(request.data)
    # print("############################################################")
    # print("REQUEST.data: {0}".format(request.data))
    # print("REQUEST: {0}".format(request))
    # print("ARGS: {0}".format(request.args))
    # print("FORM: {0}".format(request.form))
    # print("FILES: {0}".format(request.files))
    # print("VALUES: {0}".format(request.values))
    # print("############################################################")
    if webhook['data']['personEmail'] != BOT_EMAIL: # TODO access config vars here
        query_url = webex.sendGetRequest(SPARK_MESSAGES_URL + webhook['data']['id']) # TODO access config vars here
        query_url = json.loads(query_url)
        # TODO connector to ray's segment
        out_message = ""
        webex.sendPostRequest(SPARK_MESSAGES_URL, # TODO access config here
            {
                "roomId": webhook['data']['roomId'],
                "text": out_message,
                "files": ["https://i.redd.it/ho7von2212w11.jpg"]
            })
    return "true"

if __name__ == "__main__":
    app.run()
