from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class TextMessageSignUp(models.Model):
    created = models.DateTimeField("creation date", auto_now_add=True)
    changed = models.DateTimeField("last modified", auto_now=True)
    opted_in = models.BooleanField("opted in")
    phone_number = PhoneNumberField("phone number", blank=True)

    class Meta:
        verbose_name = "text message sign up"

    def __str__(self):
        return f"{self.phone_number} (opted {'in' if self.opted_in else 'out'})"


class TextMessage(models.Model):
    created = models.DateTimeField("received date", auto_now_add=True, db_index=True)
    phone_number = PhoneNumberField("phone number")
    message = models.TextField()

    class Meta:
        verbose_name = "Text message"
        ordering = ("-created",)

    def __str__(self):
        return f"Message from {self.phone}"
