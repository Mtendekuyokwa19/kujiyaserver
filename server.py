from flask import Flask, request
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
app = Flask(__name__)


# ------------------------------------------------------------
# Optional: log every incoming request for debugging
# ------------------------------------------------------------
@app.before_request
def log_request_info():
    print(">>>", request.method, request.url)
    print("Headers:", request.headers)
    print("Body:", request.get_data(as_text=True))


# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------
@app.route("/")
def hello_world():
    # Root path – only for testing in a browser
    return "<p>Hello, World!</p>"


@app.route("/sms_call", methods=["POST"])
def sms_call():
    """
    Africa's Talking will POST incoming SMS or delivery reports here.
    """
    # Print all form fields received from Africa's Talking
    print("Incoming POST data:", request.form)

    # Always return a 200-series status so Africa's Talking knows
    # the callback was successfully received.
    respondsms(request.form["from"], "yes I have received", request.form["linkId"])
    return "OK", 200


# ------------------------------------------------------------
# SMS sending helper class
# ------------------------------------------------------------
SANDBOXAPI = config["SANDBOXAPI"]


def respondsms(phonenumber, message, linkid):

    payload = {
        "username": "sandbox",
        "to": ["+265983342542"],
        "message": "yes I have received",
        "from": "56787",
        linkid: linkid,
    }
    headers = {
        "apiKey": SANDBOXAPI,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    r = requests.post(
        "https://api.sandbox.africastalking.com/version1/messaging",
        data=payload,
        headers=headers,
    )
    print("SMS API response:", r.status_code, r.text)
