import logging
import re
from smtplib import SMTPException

from twilio.twiml.messaging_response import MessagingResponse
from unidecode import unidecode

from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View

from jew_pizza.twilio import twilio_request
from jew_pizza.utils import get_client_ip

from .forms import ContactForm, NewsletterForm
from .models import TextMessage
from .utils import sign_up_for_substack


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


class FormInvalidErrorMixin:
    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please correct it below.")
        return super().form_invalid(form)


class ContactView(SuccessMessageMixin, FormInvalidErrorMixin, FormView):
    extra_context = {"title": "Contact"}
    form_class = ContactForm
    success_message = "Your email has successfully been sent to David. Give him a little while to respond. Thanks!"
    success_url = reverse_lazy("webcore:home")
    template_name = "notifications/contact.html"

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]
        substack_sign_up = form.cleaned_data.get("substack_sign_up")
        ip_address = get_client_ip(self.request)

        try:
            send_mail(
                subject=f"{name} - jew.pizza Contact Form",
                message=(
                    f"Name: {name}\nEmail: {email}\nNewsletter sign-up: {'yes' if substack_sign_up else 'no'}\n"
                    f"IP: {ip_address}\n\nMessage:\n{message}"
                ),
                from_email=None,
                recipient_list=[settings.EMAIL_ADDRESS],
            )
        except SMTPException:
            messages.error(
                self.request,
                "An error occurred while sending your email. Try again or send your message to"
                f" {settings.EMAIL_ADDRESS} directly.",
            )
            django_logger = logging.getLogger("django.request")
            django_logger.exception("An error occurred while sending an email via the contact form.")

        if substack_sign_up:
            sign_up_for_substack(email, request=self.request)

        return super().form_valid(form)


class NewsletterView(FormInvalidErrorMixin, FormView):
    extra_context = {"title": "Newsletter"}
    form_class = NewsletterForm
    success_url = reverse_lazy("webcore:home")
    template_name = "notifications/newsletter.html"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        if not sign_up_for_substack(email, request=self.request):
            # Downgrade gracefully
            return redirect("notifications:newsletter-iframe")
        return super().form_valid(form)
