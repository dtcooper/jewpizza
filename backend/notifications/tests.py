from smtplib import SMTPException
from unittest.mock import patch

from django.contrib import messages
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import SignUp


class SignUpTests(TestCase):
    def assertMessage(self, response, level, message):
        msgs = messages.get_messages(response.wsgi_request)
        for msg in msgs:
            if msg.level == level and msg.message == message:
                break
        else:
            actual = "\n  ".join(f"[{messages.constants.DEFAULT_TAGS.get(msg.level)}] {msg.message!r}" for msg in msgs)
            tag = messages.constants.DEFAULT_TAGS.get(level)
            self.fail(f"No message found: [{tag}] {message!r}. Got messages: [\n  {actual}\n]")

    def reset_mocks(self):
        mail.outbox = []
        self.sms_mock.reset_mock()

    def setUp(self):
        self.sms_patcher = patch("notifications.views.send_sms")
        self.sms_mock = self.sms_patcher.start()

    def tearDown(self):
        self.sms_patcher.stop()

    def test_renders(self):
        response = self.client.get(reverse("notifications:sign-up"))
        self.assertEqual(response.status_code, 200)

    def test_new_email_only(self):
        self.assertEqual(SignUp.objects.count(), 0)
        response = self.client.post(reverse("notifications:sign-up"), {"email": "david@jew.pizza"})
        self.assertRedirects(response, reverse("webcore:home"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.UNCONFIRMED)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertIsInstance(sign_up.phone, str)
        self.assertEqual(sign_up.phone, "")
        self.assertMessage(
            response,
            messages.SUCCESS,
            "You're almost signed up for for notifications. Please check your email to confirm.",
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients(), ["david@jew.pizza"])
        self.sms_mock.assert_not_called()

    def test_existing_email_only_unconfirmed(self):
        SignUp.objects.create(email="david@jew.pizza")
        self.assertEqual(SignUp.objects.count(), 1)
        response = self.client.post(reverse("notifications:sign-up"), {"email": "david@jew.pizza"})
        self.assertRedirects(response, reverse("webcore:home"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.UNCONFIRMED)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertIsInstance(sign_up.phone, str)
        self.assertEqual(sign_up.phone, "")
        self.assertMessage(
            response,
            messages.SUCCESS,
            "You're almost signed up for for notifications. Please check your email to confirm.",
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients(), ["david@jew.pizza"])
        self.sms_mock.assert_not_called()

    def test_existing_email_only_confirmed(self):
        SignUp.objects.create(email="david@jew.pizza", status=SignUp.Status.EMAIL)
        self.assertEqual(SignUp.objects.count(), 1)
        response = self.client.post(reverse("notifications:sign-up"), {"email": "david@jew.pizza"})
        self.assertRedirects(response, reverse("notifications:sign-up"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.EMAIL)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertIsInstance(sign_up.phone, str)
        self.assertEqual(sign_up.phone, "")
        self.assertMessage(response, messages.INFO, "You were already signed up for notifications.")
        self.assertEqual(len(mail.outbox), 0)
        self.sms_mock.assert_not_called()

    def test_new_email_and_phone(self):
        self.assertEqual(SignUp.objects.count(), 0)
        response = self.client.post(
            reverse("notifications:sign-up"),
            {
                "email": "david@jew.pizza",
                "with_phone": True,
                "phone": "+1 (212) 555-1234",
            },
        )
        self.assertRedirects(response, reverse("webcore:home"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.UNCONFIRMED)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertEqual(sign_up.phone, "+12125551234")
        self.assertMessage(
            response,
            messages.SUCCESS,
            "You're almost signed up for for notifications. Please check your email and mobile phone to confirm.",
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients(), ["david@jew.pizza"])
        self.sms_mock.assert_called_once()

    def test_existing_email_and_phone_unconfirmed(self):
        SignUp.objects.create(email="david@jew.pizza", phone="+12125551234")
        self.assertEqual(SignUp.objects.count(), 1)
        response = self.client.post(
            reverse("notifications:sign-up"),
            {
                "email": "david@jew.pizza",
                "with_phone": True,
                "phone": "+1 (212) 555-1234",
            },
        )
        self.assertRedirects(response, reverse("webcore:home"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.UNCONFIRMED)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertEqual(sign_up.phone, "+12125551234")
        self.assertMessage(
            response,
            messages.SUCCESS,
            "You're almost signed up for for notifications. Please check your email and mobile phone to confirm.",
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients(), ["david@jew.pizza"])
        self.sms_mock.assert_called_once()

    def test_existing_email_and_phone_confirmed(self):
        SignUp.objects.create(email="david@jew.pizza", phone="+12125551234", status=SignUp.Status.BOTH)
        self.assertEqual(SignUp.objects.count(), 1)
        response = self.client.post(
            reverse("notifications:sign-up"),
            {
                "email": "david@jew.pizza",
                "with_phone": True,
                "phone": "+1 (212) 555-1234",
            },
        )
        self.assertRedirects(response, reverse("notifications:sign-up"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.BOTH)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertEqual(sign_up.phone, "+12125551234")
        self.assertMessage(response, messages.INFO, "You were already signed up for notifications.")
        self.assertEqual(len(mail.outbox), 0)
        self.sms_mock.assert_not_called()

        self.reset_mocks()
        SignUp.objects.update(status=SignUp.Status.EMAIL)
        response = self.client.post(
            reverse("notifications:sign-up"),
            {
                "email": "david@jew.pizza",
                "with_phone": True,
                "phone": "+1 (212) 555-1234",
            },
        )
        self.assertRedirects(response, reverse("webcore:home"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.EMAIL)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertEqual(sign_up.phone, "+12125551234")
        self.assertMessage(
            response,
            messages.SUCCESS,
            "You're almost signed up for for notifications. Please check your mobile phone to confirm.",
        )
        self.assertEqual(len(mail.outbox), 0)
        self.sms_mock.assert_called_once()

        self.reset_mocks()
        SignUp.objects.update(status=SignUp.Status.SMS)
        response = self.client.post(
            reverse("notifications:sign-up"),
            {
                "email": "david@jew.pizza",
                "with_phone": True,
                "phone": "+1 (212) 555-1234",
            },
        )
        self.assertRedirects(response, reverse("webcore:home"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.SMS)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertEqual(sign_up.phone, "+12125551234")
        self.assertMessage(
            response,
            messages.SUCCESS,
            "You're almost signed up for for notifications. Please check your email to confirm.",
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients(), ["david@jew.pizza"])
        self.sms_mock.assert_not_called()

    def test_existing_email_add_phone(self):
        SignUp.objects.create(email="david@jew.pizza")
        self.assertEqual(SignUp.objects.count(), 1)
        response = self.client.post(
            reverse("notifications:sign-up"),
            {
                "email": "david@jew.pizza",
                "with_phone": True,
                "phone": "+1 (212) 555-1234",
            },
        )
        self.assertRedirects(response, reverse("webcore:home"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.UNCONFIRMED)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertEqual(sign_up.phone, "+12125551234")
        self.assertMessage(
            response,
            messages.SUCCESS,
            "You're almost signed up for for notifications. Please check your email and mobile phone to confirm.",
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients(), ["david@jew.pizza"])
        self.sms_mock.assert_called_once()

        self.reset_mocks()
        SignUp.objects.update(status=SignUp.Status.EMAIL)
        response = self.client.post(
            reverse("notifications:sign-up"),
            {
                "email": "david@jew.pizza",
                "with_phone": True,
                "phone": "+1 (212) 555-1234",
            },
        )
        self.assertRedirects(response, reverse("webcore:home"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.EMAIL)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertEqual(sign_up.phone, "+12125551234")
        self.assertMessage(
            response,
            messages.SUCCESS,
            "You're almost signed up for for notifications. Please check your mobile phone to confirm.",
        )
        self.assertEqual(len(mail.outbox), 0)
        self.sms_mock.assert_called_once()

    def test_exising_email_and_phone_change_phone(self):
        SignUp.objects.create(email="david@jew.pizza", phone="+12125551234")
        self.assertEqual(SignUp.objects.count(), 1)

        for status in (SignUp.Status.UNCONFIRMED, SignUp.Status.SMS):
            self.reset_mocks()
            SignUp.objects.update(phone="+12125551234", status=status)
            response = self.client.post(
                reverse("notifications:sign-up"),
                {
                    "email": "david@jew.pizza",
                    "with_phone": True,
                    "phone": "+1 (212) 555-4321",
                },
            )
            self.assertRedirects(response, reverse("webcore:home"))
            self.assertEqual(SignUp.objects.count(), 1)
            sign_up = SignUp.objects.get()
            self.assertEqual(sign_up.status, SignUp.Status.UNCONFIRMED)
            self.assertEqual(sign_up.email, "david@jew.pizza")
            self.assertEqual(sign_up.phone, "+12125554321")
            self.assertMessage(
                response,
                messages.SUCCESS,
                "You're almost signed up for for notifications. Please check your email and mobile phone to confirm.",
            )
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].recipients(), ["david@jew.pizza"])
            self.sms_mock.assert_called_once()

        for status in (SignUp.Status.EMAIL, SignUp.Status.BOTH):
            self.reset_mocks()
            SignUp.objects.update(phone="+12125551234", status=status)
            response = self.client.post(
                reverse("notifications:sign-up"),
                {
                    "email": "david@jew.pizza",
                    "with_phone": True,
                    "phone": "+1 (212) 555-4321",
                },
            )
            self.assertRedirects(response, reverse("webcore:home"))
            self.assertEqual(SignUp.objects.count(), 1)
            sign_up = SignUp.objects.get()
            self.assertEqual(sign_up.status, SignUp.Status.EMAIL)
            self.assertEqual(sign_up.email, "david@jew.pizza")
            self.assertEqual(sign_up.phone, "+12125554321")
            self.assertMessage(
                response,
                messages.SUCCESS,
                "You're almost signed up for for notifications. Please check your mobile phone to confirm.",
            )
            self.assertEqual(len(mail.outbox), 0)
            self.sms_mock.assert_called_once()

    def test_exising_email_and_phone_remove_phone(self):
        SignUp.objects.create(email="david@jew.pizza", phone="+12125551234")
        self.assertEqual(SignUp.objects.count(), 1)

        for status in (SignUp.Status.UNCONFIRMED, SignUp.Status.SMS):
            self.reset_mocks()
            SignUp.objects.update(phone="+12125551234", status=status)
            response = self.client.post(
                reverse("notifications:sign-up"),
                {"email": "david@jew.pizza", "phone": "+1 (212) 555-4321"},
            )
            self.assertRedirects(response, reverse("webcore:home"))
            self.assertEqual(SignUp.objects.count(), 1)
            sign_up = SignUp.objects.get()
            self.assertEqual(sign_up.status, SignUp.Status.UNCONFIRMED)
            self.assertEqual(sign_up.email, "david@jew.pizza")
            self.assertIsInstance(sign_up.phone, str)
            self.assertEqual(sign_up.phone, "")
            self.assertMessage(
                response,
                messages.SUCCESS,
                "You're almost signed up for for notifications. Please check your email to confirm.",
            )
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].recipients(), ["david@jew.pizza"])
            self.sms_mock.assert_not_called()

        self.reset_mocks()
        SignUp.objects.update(phone="+12125551234", status=SignUp.Status.BOTH)
        response = self.client.post(
            reverse("notifications:sign-up"),
            {"email": "david@jew.pizza", "phone": "+1 (212) 555-4321"},
        )
        self.assertRedirects(response, reverse("notifications:sign-up"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.EMAIL)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertIsInstance(sign_up.phone, str)
        self.assertEqual(sign_up.phone, "")
        self.assertMessage(response, messages.INFO, "You were already signed up for notifications.")
        self.assertEqual(len(mail.outbox), 0)
        self.sms_mock.assert_not_called()

    def test_opt_out(self):
        SignUp.objects.create(email="david@jew.pizza", phone="+12125551234")
        self.assertEqual(SignUp.objects.count(), 1)

        for status in (
            SignUp.Status.UNCONFIRMED,
            SignUp.Status.SMS,
            SignUp.Status.EMAIL,
            SignUp.Status.BOTH,
        ):
            SignUp.objects.update(status=status)
            response = self.client.post(
                reverse("notifications:sign-up"),
                {"email": "david@jew.pizza", "opt_out": True},
            )
            self.assertRedirects(response, reverse("notifications:sign-up"))
            self.assertEqual(SignUp.objects.count(), 1)
            sign_up = SignUp.objects.get()
            self.assertEqual(sign_up.status, SignUp.Status.OPTED_OUT)
            self.assertEqual(sign_up.email, "david@jew.pizza")
            self.assertEqual(sign_up.phone, "+12125551234")
            self.assertMessage(
                response,
                messages.INFO,
                "We've successfully unsubscribed you from notifications.",
            )
            self.assertEqual(len(mail.outbox), 0)
            self.sms_mock.assert_not_called()

    def test_existing_email_and_phone_opt_back_in(self):
        SignUp.objects.create(
            email="david@jew.pizza",
            phone="+12125551234",
            status=SignUp.Status.OPTED_OUT,
        )
        self.assertEqual(SignUp.objects.count(), 1)

        response = self.client.post(
            reverse("notifications:sign-up"),
            {"email": "david@jew.pizza", "with_phone": True, "phone": "+12125551234"},
        )
        self.assertRedirects(response, reverse("webcore:home"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.UNCONFIRMED)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertEqual(sign_up.phone, "+12125551234")
        self.assertMessage(
            response,
            messages.SUCCESS,
            "You're almost signed up for for notifications. Please check your email and mobile phone to confirm.",
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients(), ["david@jew.pizza"])
        self.sms_mock.assert_called_once()

    def test_existing_email_only_opt_back_in(self):
        SignUp.objects.create(
            email="david@jew.pizza",
            phone="+12125551234",
            status=SignUp.Status.OPTED_OUT,
        )
        self.assertEqual(SignUp.objects.count(), 1)

        response = self.client.post(reverse("notifications:sign-up"), {"email": "david@jew.pizza"})
        self.assertRedirects(response, reverse("webcore:home"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.UNCONFIRMED)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertIsInstance(sign_up.phone, str)
        self.assertEqual(sign_up.phone, "")
        self.assertMessage(
            response,
            messages.SUCCESS,
            "You're almost signed up for for notifications. Please check your email to confirm.",
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients(), ["david@jew.pizza"])
        self.sms_mock.assert_not_called()

    def test_no_phone_number_shows_error(self):
        response = self.client.post(reverse("notifications:sign-up"), {"email": "david@jew.pizza", "with_phone": True})
        self.assertEqual(SignUp.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)
        form = response.context_data["form"]
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("phone"))
        self.assertIn("A phone number is required.", form.errors["phone"])

    def test_opt_out_with_no_sign_up_shows_error(self):
        response = self.client.post(reverse("notifications:sign-up"), {"email": "david@jew.pizza", "opt_out": True})
        self.assertEqual(SignUp.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)
        form = response.context_data["form"]
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("__all__"))
        self.assertIn("Sign up with this email address does not exist. Can't opt out.", form.errors["__all__"])

    def test_phone_number_too_expensive(self):
        # Gabon (GA)
        response = self.client.post(
            reverse("notifications:sign-up"), {"email": "david@jew.pizza", "with_phone": True, "phone": "+24101694321"}
        )
        self.assertEqual(SignUp.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)
        form = response.context_data["form"]
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("phone"))
        self.assertIn(
            "You country (GA) does not support text message notifications. Try another number.", form.errors["phone"]
        )

    @patch("notifications.views.send_mail", side_effect=SMTPException)
    def test_email_failure(self, send_mail_mock):
        self.assertEqual(SignUp.objects.count(), 0)
        response = self.client.post(reverse("notifications:sign-up"), {"email": "david@jew.pizza"})
        self.assertRedirects(response, reverse("webcore:home"))
        self.assertEqual(SignUp.objects.count(), 1)
        sign_up = SignUp.objects.get()
        self.assertEqual(sign_up.status, SignUp.Status.UNCONFIRMED)
        self.assertEqual(sign_up.email, "david@jew.pizza")
        self.assertIsInstance(sign_up.phone, str)
        self.assertEqual(sign_up.phone, "")
        send_mail_mock.assert_called_once()
        self.assertEqual(len(mail.outbox), 0)
        self.assertMessage(response, messages.ERROR, "An error occurred while sending you an email. Please try again.")
        self.sms_mock.assert_not_called()
