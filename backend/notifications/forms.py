from phonenumbers import region_code_for_number

from django import forms
from django.core.exceptions import ValidationError

from phonenumber_field.formfields import PhoneNumberField

from .constants import ALLOWED_SMS_COUNTRIES
from .models import SignUp


class SignUpForm(forms.Form):
    email = forms.EmailField(
        label="Email Address", max_length=SignUp._meta.get_field("email").max_length, required=True
    )
    phone = PhoneNumberField(
        label="Phone Number", max_length=SignUp._meta.get_field("phone").max_length, required=False
    )
    opt_out = forms.BooleanField(initial=False, required=False)
    with_phone = forms.BooleanField(
        label="Receive notifications by phone (SMS). [Data rates may apply.]", initial=False, required=False
    )

    def __init__(self, *args, **kwargs):
        self.existing_sign_up = None
        super().__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if phone:
            country = region_code_for_number(phone)
            if country not in ALLOWED_SMS_COUNTRIES:
                raise ValidationError(
                    f"You country ({country}) does not support text message notifications. Try another number."
                )

        return phone

    def clean(self):
        cleaned_data = super().clean()

        if not self.errors:
            if self.cleaned_data.get("with_phone") and not self.cleaned_data.get("phone"):
                raise ValidationError({"phone": "A phone number is required."})

            try:
                self.existing_sign_up = SignUp.objects.get(email=cleaned_data["email"])
            except SignUp.DoesNotExist:
                pass

            if cleaned_data.get("opt_out") and not self.existing_sign_up:
                raise ValidationError("Sign up with this email address does not exist. Can't opt out.")
