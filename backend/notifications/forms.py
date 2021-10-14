from django import forms
from django.utils.safestring import mark_safe


class NewsletterForm(forms.Form):
    email = forms.EmailField(label="Email Address")


class ContactForm(forms.Form):
    name = forms.CharField(label="Name", max_length=255)
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(label="Your Message", widget=forms.Textarea)
    substack_sign_up = forms.BooleanField(
        label=mark_safe('<span class="italic">Sign me up for David\'s newsletter!</span>'), required=False, initial=True
    )
