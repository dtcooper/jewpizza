from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "notifications"
urlpatterns = [
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("newsletter/", views.NewsletterView.as_view(), name="newsletter"),
    path(
        "newsletter/iframe/",
        TemplateView.as_view(
            template_name="notifications/newsletter.html", extra_context={"title": "Newsletter", "form": None}
        ),
        name="newsletter-iframe",
    ),
    path("twilio/incoming-sms/", views.IncomingTextMessageView.as_view(), name="incoming-sms"),
]
