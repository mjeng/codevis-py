from urllib.request import Request, urlopen

# TODO move these to config vars
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
