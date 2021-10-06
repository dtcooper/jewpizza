from smtplib import SMTPException

from twilio.twiml.messaging_response import MessagingResponse

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, RedirectView

from jew_pizza.twilio import send_sms, twilio_validator
from webcore.views import TemplateOrJSONViewMixin

from .forms import SendNotificationAdminForm, SignUpForm
from .models import SignUp, TextMessage


class SendNotificationAdminView(UserPassesTestMixin, SuccessMessageMixin, FormView):
    form_class = SendNotificationAdminForm
    template_name = 'notifications/send_notification.html'
    success_message = 'The notification was successfully sent.'
    success_url = reverse_lazy('admin:notifications_signup_changelist')
    extra_context = {'title': 'Send Notification', 'site_header': admin.site.site_header, 'has_permission': True, 'site_url': admin.site.site_url}

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        email_subject = form.cleaned_data.get('email_subject', '').strip()
        email_message = form.cleaned_data.get('email_message', '').strip()
        text_message = form.cleaned_data.get('text_message', '').strip()

        if email_subject and email_message:
            emails = SignUp.objects.filter(status__in=(SignUp.Status.EMAIL, SignUp.Status.BOTH)).values_list('email', flat=True)
            for email in emails:
                send_mail(subject=email_subject, message=email_message, from_email=None, recipient_list=[email])

        if text_message:
            phones = SignUp.objects.exclude(phone='').filter(status__in=(SignUp.Status.SMS, SignUp.Status.BOTH)).values_list('phone', flat=True).distinct()
            for phone in phones:
                send_sms(text_message, phone)

        return super().form_valid(form)


@csrf_exempt
def incoming_sms_view(request):
    if settings.DEBUG or twilio_validator.validate(
        request.build_absolute_uri(), request.POST, request.META.get("HTTP_X_TWILIO_SIGNATURE", "")
    ):
        message = request.POST.get("Body", "")
        phone = request.POST.get("From", "")

        if phone and message:
            TextMessage.objects.create(phone=phone, message=message)

        if phone and ("yes" in message.lower() or "subscribe" in message.lower()):
            # Move to SignUp.apply_sms_response() or something
            sign_ups = SignUp.objects.filter(phone=phone).exclude(status=SignUp.Status.OPTED_OUT)
            if sign_ups.exists():
                did_sign_up = False

                for sign_up in sign_ups:
                    status_before = sign_up.status
                    if sign_up.status == SignUp.Status.UNCONFIRMED:
                        sign_up.status = SignUp.Status.SMS
                    elif sign_up.status == SignUp.Status.EMAIL:
                        sign_up.status = SignUp.Status.BOTH

                    if sign_up.status != status_before:
                        did_sign_up = True
                        sign_up.save()

                response = MessagingResponse()
                url = request.build_absolute_uri(reverse("notifications:sign-up"))
                if did_sign_up:
                    response.message(
                        f"You have successfully signed up for jew.pizza notifications! Reply STOP or visit {url} to"
                        " unsubscribe."
                    )
                else:
                    response.message(
                        f"You are already signed up for notifications. Reply STOP or visit {url} to unsubscribe."
                    )
                return HttpResponse(str(response), content_type="text/xml")

        return HttpResponse(status=204)
    else:
        return HttpResponseForbidden()


class SignUpConfirmationView(RedirectView):
    pattern_name = "webcore:home"
    max_token_age = 60 * 60 * 12  # 12 hours

    def get_redirect_url(self, token, *args, **kwargs):
        if SignUp.apply_token(token):
            messages.success(self.request, "You have successfully signed up for email notifications!")
        else:
            messages.warning(self.request, "That link was invalid. You might try signing up for notifications again.")
            self.pattern_name = "notifications:sign-up"

        return super().get_redirect_url(*args, **kwargs)


class SignUpView(TemplateOrJSONViewMixin, FormView):
    form_class = SignUpForm
    template_name = "notifications/sign-up.html"
    extra_context = {"title": "Notify Me", "hide_title": True}
    fields = "__all__"
    success_url = reverse_lazy("webcore:home")

    def form_valid(self, form):
        sign_up = form.existing_sign_up
        with_phone, opt_out = (
            form.cleaned_data["with_phone"],
            form.cleaned_data["opt_out"],
        )
        email, phone = form.cleaned_data["email"], form.cleaned_data["phone"]
        should_send_mail = should_send_sms = False

        if opt_out:
            sign_up.status = SignUp.Status.OPTED_OUT
            sign_up.save()

            messages.info(self.request, "We've successfully unsubscribed you from notifications.")
            self.success_url = reverse("notifications:sign-up")

        else:
            if sign_up:
                # If we've opted out, opt back in and send SMS confirmation if we've got a phone number
                if sign_up.status == SignUp.Status.OPTED_OUT:
                    sign_up.status = SignUp.Status.UNCONFIRMED

                # Otherwise if we've got a phone number AND there's a change to the phone number, then
                # send SMS confirmation, and set status to unconfirm phone
                elif with_phone and sign_up.phone != phone:
                    if sign_up.status == SignUp.Status.SMS:
                        sign_up.status = SignUp.Status.UNCONFIRMED
                    elif sign_up.status == SignUp.Status.BOTH:
                        sign_up.status = SignUp.Status.EMAIL

                elif not with_phone:
                    if sign_up.status == SignUp.Status.SMS:
                        sign_up.status = SignUp.Status.UNCONFIRMED
                    elif sign_up.status == SignUp.Status.BOTH:
                        sign_up.status = SignUp.Status.EMAIL

                # Set phone number to blank if we're not providing it
                sign_up.phone = phone if with_phone else ""

                # If we're still unconfirmed by email, re-send it
                if sign_up.status in (SignUp.Status.UNCONFIRMED, SignUp.Status.SMS):
                    should_send_mail = True
                if with_phone and sign_up.status in (SignUp.Status.UNCONFIRMED, SignUp.Status.EMAIL):
                    should_send_sms = True

                sign_up.save()

            else:
                should_send_mail = True
                kwargs = {"email": email}
                if with_phone:
                    should_send_sms = True
                    kwargs["phone"] = phone

                sign_up = SignUp.objects.create(**kwargs)

            if should_send_mail and should_send_sms:
                messages.success(
                    self.request,
                    "You're almost signed up for for notifications. Please check your email and mobile phone to"
                    " confirm.",
                )
            elif should_send_mail:
                messages.success(
                    self.request,
                    "You're almost signed up for for notifications. Please check your email to confirm.",
                )
            elif should_send_sms:
                messages.success(
                    self.request,
                    "You're almost signed up for for notifications. Please check your mobile phone to confirm.",
                )
            else:
                messages.info(self.request, "You were already signed up for notifications.")
                self.success_url = reverse("notifications:sign-up")

            if should_send_mail:
                token = SignUp.TOKEN_SIGNER.sign(str(sign_up.id))
                confirm_url = self.request.build_absolute_uri(
                    reverse("notifications:sign-up-confirm", kwargs={"token": token})
                )

                try:
                    send_mail(
                        subject="Confirm jew.pizza Sign-up",
                        message=(
                            "Dear Friend,\n\nYou have been signed up for jew.pizza notifications and the occasional"
                            " newsletter. You must confirm your email address at the link below to enable them."
                            f" \n\n{confirm_url}\n\nIf you did not sign up, you can safely ignore this"
                            " email.\n\nFondly,\nDavid Cooper"
                        ),
                        from_email=None,
                        recipient_list=[sign_up.email],
                    )

                except SMTPException:
                    messages.error(self.request, "An error occurred while sending you an email. Please try again.")

            if should_send_sms:
                if not send_sms(
                    message=(
                        'You\'ve been signed up for jew.pizza notifications. You must reply "YES" to enable them.'
                        " Msg+data rates may apply."
                    ),
                    number=sign_up.phone.as_e164,
                ):
                    messages.error(
                        self.request, "An error occurred while sending you a text message. Please try again."
                    )

        return super().form_valid(form)
