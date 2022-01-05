import hashlib

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from constance import config

from jew_pizza.twilio import send_sms

from .forms import SendEmailForm, SendTextMessageForm


NAVIGATION_VIEWS = (
    ("index", "Tools Index"),
    ("send-text-message", "Send Text Message"),
    ("send-email", "Send Email"),
    ("sse-status", "SSE Status"),
)
NAVIGATION_EXT_LINKS = (
    (lambda: config.LOGS_URL, "Service Logs"),
    (lambda: config.UMAMI_URL, "Analytics"),
)


class AdminToolsViewMixin:
    title = None

    @classmethod
    def as_view(cls, title=None, *args, **kwargs):
        if title is not None or cls.title is not None:
            extra_context = kwargs.setdefault("extra_context", {})
            extra_context["title"] = title or cls.title
        return super().as_view(*args, **kwargs)

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        nav_links = []
        for url_name, name in NAVIGATION_VIEWS:
            nav_links.append((reverse(f"admin-tools:{url_name}"), name, False))
        for url_func, name in NAVIGATION_EXT_LINKS:
            nav_links.append((url_func(), name, True))
        return {"admin_nav_links": nav_links, **super().get_context_data(**kwargs)}


class AdminTemplateView(AdminToolsViewMixin, TemplateView):
    template_name = "admin_tools/base.html"


class AdminFormView(AdminToolsViewMixin, FormView):
    template_name = "admin_tools/form.html"


class SendTextMessageView(AdminFormView):
    extra_context = {"submit_text": "Send Text Message"}
    form_class = SendTextMessageForm
    success_url = reverse_lazy("admin-tools:send-text-message")
    template_name = "admin_tools/send_text_message.html"
    title = "Send Text Message"

    def form_valid(self, form):
        message = form.cleaned_data["message"]
        audience = form.cleaned_data["audience"]
        if audience == "single":
            phone_number = form.cleaned_data["phone_number"]
            if send_sms(message, phone_number):
                messages.success(self.request, "Your message has been sent!")
            else:
                messages.error(self.request, "Error sending text message. Check server logs.")
        else:
            # XXX TODO
            messages.warning(self.request, "Sign up messages not yet implemented.")

        return super().form_valid(form)


class SendEmailView(SuccessMessageMixin, AdminFormView):
    extra_context = {"submit_text": "Send Email"}
    form_class = SendEmailForm
    success_message = "The email was sent!"
    success_url = reverse_lazy("admin-tools:send-email")
    title = "Send Email"

    def form_valid(self, form):
        recipient = form.cleaned_data["recipient"]
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]
        send_mail(subject=subject, message=message, from_email=None, recipient_list=[recipient])
        return super().form_valid(form)


class SSEStatusView(AdminTemplateView):
    template_name = "admin_tools/sse_status.html"
    title = "SSE Status"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # At least if the secret key is exposed somehow, it's a SHA256 of it, not the actual key
        context["secret_key"] = hashlib.sha256(settings.SECRET_KEY.encode()).hexdigest()
        return context
