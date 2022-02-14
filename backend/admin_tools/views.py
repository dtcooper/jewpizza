from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView, View

from jew_pizza.twilio import send_sms

from .forms import SendEmailForm, SendTextMessageForm


NAVIGATION_LINKS = (
    (reverse_lazy("admin-tools:index"), "Tools Index", False),
    (reverse_lazy("admin-tools:send-text-message"), "Send Text Message", False),
    (reverse_lazy("admin-tools:send-email"), "Send Email", False),
    (reverse_lazy("admin-tools:sse-status"), "SSE Status", False),
    (reverse_lazy("admin-tools:nginx-internal", kwargs={"module": "logs"}), "Service Logs", True),
    (f"//{settings.UMAMI_HOST}/", "Analytics", True),
    (reverse_lazy("admin-tools:nginx-internal", kwargs={"module": "nchan"}), "nchan Status", True),
)


@method_decorator(staff_member_required, name="dispatch")
class AdminToolsViewMixin:
    title = None

    @classmethod
    def as_view(cls, title=None, *args, **kwargs):
        if title is not None or cls.title is not None:
            extra_context = kwargs.setdefault("extra_context", {})
            extra_context["title"] = title or cls.title
        return super().as_view(*args, **kwargs)

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


@method_decorator(staff_member_required, name="dispatch")
class NginxInternalView(View):
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse(headers={"X-Accel-Redirect": f"/protected{request.get_full_path()}"})
