from flask import Flask, request, render_template, abort
from requests_toolbelt import MultipartEncoder
import json, io
import parse_file, webex

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("homepage.html")

# TODO move these to config vars
BOT_EMAIL = "codevis@webex.bot"
SPARK_MESSAGES_URL = "https://api.ciscospark.com/v1/messages/"

@app.route("/webex", methods=["POST"])
def webex_request():
    webhook = json.loads(request.data)
    if webhook['data']['personEmail'] != BOT_EMAIL: # TODO access config vars here
        request_json = webex.sendGetRequest(SPARK_MESSAGES_URL + webhook['data']['id']) # TODO access config vars here
        query_url = json.loads(request_json).get("text")
        if query_url is None:
            abort(400, "No URL sent")

        try:
            im = parse_file.gh_link_entry(query_url)
        except AssertionError as e:
            abort(400, "Invalid URL")

        output = io.BytesIO()
        im.save(output, format="PNG")
        out_message = "Visualization of {0}".format(query_url)

        fields = {
            "roomId": webhook['data']['roomId'],
            "text": out_message,
            "files": ("visualize.png", output, "image/png")
        }
        data = MultipartEncoder(fields=fields)
        webex.sendPostRequest(SPARK_MESSAGES_URL, data)
    return "true"

if __name__ == "__main__":
    app.run()
