from functools import wraps
import logging

from twilio.base.exceptions import TwilioRestException
from twilio.request_validator import RequestValidator
from twilio.rest import Client
from twilio.twiml import TwiML

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from constance import config
from phonenumber_field.phonenumber import PhoneNumber


twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
twilio_validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
logger = logging.getLogger(f'jewpizza.{__file__}')


def send_sms(message, phone_number):
    try:
        if isinstance(phone_number, PhoneNumber):
            phone_number = phone_number.as_e164
        from_number = config.TWILIO_FROM_NUMBER
        if isinstance(from_number, PhoneNumber):
            from_number = from_number.as_e164

        twilio_client.messages.create(to=phone_number, from_=from_number, body=message)
        return True
    except TwilioRestException:
        logger.exception('Error sending test message')
        return False


def twilio_request(view):
    @wraps(view)
    def decorated_view(request, *args, **kwargs):
        if twilio_validator.validate(
            request.build_absolute_uri(), request.POST, request.headers.get("X-Twilio-Signature", "")
        ):
            response = view(request, *args, **kwargs)
            if isinstance(response, TwiML):
                response = HttpResponse(response, content_type="text/xml")
            elif response is True:  # Special case for text messages, return empty response. True and only True.
                response = HttpResponse(status=204)
            return response
        else:
            raise PermissionDenied

    return decorated_view
