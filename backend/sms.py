import messagebird
from twilio.rest import Client



# --- Twilio Configuration ---
# TWILIO_ACCOUNT_SID = "AC3d1820a310433f6620ce1267cfcc4a1a" # os.environ["TWILIO_ACCOUNT_SID"]
# TWILIO_AUTH_TOKEN = "90140fb37355d632037044f5be615eeb" # os.environ["TWILIO_AUTH_TOKEN"]
# TWILIO_PHONE_NUMBER = "+18887714296" # os.environ["TWILIO_PHONE_NUMBER"]

# # look at logs at https://console.twilio.com/us1/monitor/logs/sms
# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
# verification_code = "123456"
# message = client.messages.create(
#     to='+15109968018',
#     from_=TWILIO_PHONE_NUMBER,
#     body=f"Your verification code is: {verification_code}",
# )
# print(message)
# me = message
# import pdb; pdb.set_trace()


client = messagebird.Client('CZvDulL95NjXWtV6KDwxBihdTKMrmNAIJPYh')
try:
    # Send a new message
    message = client.message_create(
        'MessageBird',  # Originator (sender name)
        '+15109968018',  # Recipient phone number (replace with the actual number)
        'Hello, this is a test message from MessageBird!',  # Message content
        {'reference': 'Foobar'}  # Optional parameters
    )
    print(f"Message sent successfully! Message ID: {message.id}")

except messagebird.client.ErrorException as e:
    print(f"An error occurred: {e}")
    for error in e.errors:
        print(f" - {error.description}")
import pdb; pdb.set_trace()