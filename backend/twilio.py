from twilio.rest import Client
# --- Twilio Configuration ---
TWILIO_ACCOUNT_SID = "AC3d1820a310433f6620ce1267cfcc4a1a" # os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = "90140fb37355d632037044f5be615eeb" # os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = "+18887714296" # os.environ["TWILIO_PHONE_NUMBER"]

# look at logs at https://console.twilio.com/us1/monitor/logs/sms

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
verification_code = "123456"
message = client.messages.create(
    to='+15109968018',
    from_=TWILIO_PHONE_NUMBER,
    body=f"Your verification code is: {verification_code}",
)
print(message)
me = message
import pdb; pdb.set_trace()