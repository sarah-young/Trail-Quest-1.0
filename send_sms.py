import secrets

from twilio.rest import Client

twilio_account_sid = secrets.TWILIO_ACCOUNT_SID
twilio_auth_token = secrets.TWILIO_AUTH_TOKEN
twilio_number = secrets.TWILIO_NUMBER

# Your Account SID from twilio.com/console
account_sid = twilio_account_sid
# Your Auth Token from twilio.com/console
auth_token  = twilio_auth_token

client = Client(account_sid, auth_token)

def send_message(phone_number, message):
    """Take in message text and forward to the phone number passed to the
    function"""

    message = client.messages.create(
        to=phone_number,
        from_=twilio_number,
        body=message)

    print(message.sid)
