from functools import wraps

from twilio.base.exceptions import TwilioRestException
from twilio.request_validator import RequestValidator
from twilio.rest import Client
from twilio.twiml import TwiML

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden

from phonenumber_field.phonenumber import PhoneNumber

twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
twilio_validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)


def send_sms(message, phone_number):
    try:
        if isinstance(phone_number, PhoneNumber):
            phone_number = phone_number.as_e164

        twilio_client.messages.create(to=phone_number, from_=settings.TWILIO_FROM_NUMBER, body=message)
        return True
    except TwilioRestException:
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
            return HttpResponseForbidden()

    return decorated_view
