from django.core import signing
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class SignUp(models.Model):
    TOKEN_SIGNER = signing.TimestampSigner(salt="signup:token", sep="/")
    TOKEN_MAX_AGE = 6 * 60 * 60  # 6 hours

    class Status(models.IntegerChoices):
        UNCONFIRMED = 0, "unconfirmed"
        EMAIL = 1, "email confirmed only"
        SMS = 2, "phone number confirmed only"
        BOTH = 3, "both email and phone number confirmed"
        OPTED_OUT = 4, "opted out"

    created = models.DateTimeField("creation date", auto_now_add=True)
    changed = models.DateTimeField("last modified", auto_now=True)
    status = models.PositiveSmallIntegerField("confirmation status", choices=Status.choices, default=Status.UNCONFIRMED)
    email = models.EmailField("email address", unique=True)
    phone = PhoneNumberField("phone number", blank=True)

    class Meta:
        verbose_name = "Notification sign up"

    def __str__(self):
        s = self.email
        if self.phone:
            s = f"{s} [{self.phone}]"
        return f"{s} - {self.get_status_display()}"

    @classmethod
    def apply_token(cls, token):
        try:
            sign_up_id = cls.TOKEN_SIGNER.unsign(token, max_age=cls.TOKEN_MAX_AGE)
            sign_up = cls.objects.get(id=sign_up_id)
        except (signing.BadSignature, cls.DoesNotExist):
            return False

        status_before = sign_up.status

        if sign_up.status == cls.Status.UNCONFIRMED:
            sign_up.status = cls.Status.EMAIL
        elif sign_up.status == cls.Status.SMS:
            sign_up.status = cls.Status.BOTH

        if status_before != sign_up.status:
            sign_up.save()
            return True
        else:
            return False


class TextMessage(models.Model):
    created = models.DateTimeField("received date", auto_now_add=True, db_index=True)
    phone = PhoneNumberField("phone number")
    message = models.TextField()

    class Meta:
        verbose_name = "Text message"
        ordering = ("-created",)

    def __str__(self):
        return f"Message from {self.phone}"
