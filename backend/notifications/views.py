import re
from smtplib import SMTPException

from twilio.twiml.messaging_response import MessagingResponse
from unidecode import unidecode

from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, FormView
from django.urls import reverse_lazy

from jew_pizza.twilio import twilio_request

from .forms import ContactForm
from .models import TextMessage


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(twilio_request, name="dispatch")
class IncomingTextMessageView(View):
    SUBSCRIBE_KEYWORDS = {"start", "yes", "subscribe", "unstop"}
    UNSUBSCRIBE_KEYWORDS = {"no", "stop", "unsubscribe"}
    WHITESPACE_RE = re.compile(r"\s+")
    NON_NORMAL_CHARS_RE = re.compile(r"[^a-zA-Z0-9 ]")

    @classmethod
    def normalize_message(cls, message):
        message = unidecode(message).lower().strip()
        message = cls.WHITESPACE_RE.sub(" ", message)
        return cls.NON_NORMAL_CHARS_RE.sub("", message)

    def post(self, request, *args, **kwargs):
        response = True
        phone_number = request.POST.get("From")
        message = request.POST.get("Body")
        normalized_words = self.normalize_message(message).split()

        if phone_number and message:
            TextMessage.objects.create(phone_number=phone_number, message=message)

        subscribe = any(word in self.SUBSCRIBE_KEYWORDS for word in normalized_words)
        unsubscribe = any(word in self.UNSUBSCRIBE_KEYWORDS for word in normalized_words)
        if subscribe or unsubscribe:
            response = MessagingResponse()
            response.message(f'You have been {"un" if unsubscribe else ""}subscribed')

        return True


class ContactView(SuccessMessageMixin, FormView):
    extra_context = {'title': 'Contact'}
    template_name = 'notifications/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('webcore:home')
    success_message = 'Your message has successfully been sent to David. Give him a little while to respond. Thanks!'

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]

        try:
            send_mail(
                subject=f'{name} - jew.pizza Contact Form',
                message=f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                from_email=None,
                recipient_list=[settings.CONTACT_FORM_TO_ADDRESS],
            )
        except SMTPException:
            messages.error(self.request, 'An error occurred while sending the message. Please try again.')

        return super().form_valid(form)
