from twilio.base.exceptions import TwilioRestException
from twilio.request_validator import RequestValidator
from twilio.rest import Client

from django.conf import settings

twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
twilio_validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)


def send_sms(message, number):
    try:
        twilio_client.messages.create(to=number, from_=settings.TWILIO_FROM_NUMBER, body=message)
        return True
    except TwilioRestException:
        return False
