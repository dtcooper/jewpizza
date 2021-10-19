from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from jew_pizza.twilio import send_sms

from .forms import SendEmailForm, SendTextMessageForm


NAVIGATION_LINKS = (
    ("admin-tools:index", "Tools Index"),
    ("admin-tools:send-text-message", "Send Text Message"),
    ("admin-tools:send-email", "Send Email"),
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
        return {"admin_nav_links": NAVIGATION_LINKS, **super().get_context_data(**kwargs)}


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
            send_sms(message, phone_number)

            messages.success(self.request, "Your message has been sent!")
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
