from smtplib import SMTPException
import re

from twilio.twiml.messaging_response import MessagingResponse
from unidecode import unidecode

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, RedirectView, View

from jew_pizza.twilio import send_sms, twilio_request

from .models import TextMessage


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(twilio_request, name='dispatch')
class IncomingTextMessageView(View):
    SUBSCRIBE_KEYWORDS = {'start', 'yes', 'subscribe', 'unstop'}
    UNSUBSCRIBE_KEYWORDS = {'no', 'stop', 'unsubscribe'}
    WHITESPACE_RE = re.compile(r'\s+')
    NON_NORMAL_CHARS_RE = re.compile(r'[^a-zA-Z0-9 ]')

    @classmethod
    def normalize_message(cls, message):
        message = unidecode(message).lower().strip()
        message = cls.WHITESPACE_RE.sub(' ', message)
        return cls.NON_NORMAL_CHARS_RE.sub('', message)

    def post(self, request, *args, **kwargs):
        response = True
        phone_number = request.POST.get('From')
        message = request.POST.get('Body')
        normalized_words = self.normalize_message(message).split()

        if phone_number and message:
            TextMessage.objects.create(phone_number=phone_number, message=message)

        subscribe = any(word in self.SUBSCRIBE_KEYWORDS for word in normalized_words)
        unsubscribe = any(word in self.UNSUBSCRIBE_KEYWORDS for word in normalized_words)
        if subscribe or unsubscribe:
            response = MessagingResponse()
            response.message(f'You have been {"un" if unsubscribe else ""}subscribed')

        return True
