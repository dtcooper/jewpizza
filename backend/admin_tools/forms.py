from django import forms
from django.core.exceptions import ValidationError

from phonenumber_field.formfields import PhoneNumberField


class SendTextMessageForm(forms.Form):
    AUDIENCE_CHOICES = (
        ("single", "Single Number"),
        ("signups", "Users Signed Up to Receive Notifications"),
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "x-model": "message", "placeholder": "Enter message body here..."})
    )
    audience = forms.ChoiceField(
        choices=AUDIENCE_CHOICES, initial="single", widget=forms.Select(attrs={"x-model": "audience"})
    )
    phone_number = PhoneNumberField(required=False)

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if not message:
            raise ValidationError("You cannot send an empty message.")
        return message

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["audience"] == "single" and not cleaned_data.get("phone_number"):
            raise ValidationError({"phone_number": "A phone number is required."})


class SendEmailForm(forms.Form):
    recipient = forms.EmailField(label="Receipient email address")
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 8}))
