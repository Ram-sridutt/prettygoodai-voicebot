import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_CALLER_NUMBER = os.getenv("TWILIO_CALLER_NUMBER")
TEST_NUMBER = os.getenv("TEST_NUMBER")

print("SID =", TWILIO_ACCOUNT_SID)
print("TOKEN =", TWILIO_AUTH_TOKEN)
print("CALLER =", TWILIO_CALLER_NUMBER)
print("TEST_NUMBER =", TEST_NUMBER)

TWIML_URL = "https://bairnish-unadministrable-aubree.ngrok-free.dev/voice"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

call = client.calls.create(
    to=TEST_NUMBER,
    from_=TWILIO_CALLER_NUMBER,
    url=TWIML_URL,
    record=True
)

print("Call initiated. SID:", call.sid)