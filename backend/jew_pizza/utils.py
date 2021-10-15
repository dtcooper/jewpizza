from django.utils.formats import date_format as django_date_format
from django.utils.timezone import localtime


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip or "[unknown]"


def format_datetime(dt, format="N j, Y g:i A"):
    return django_date_format(localtime(dt), format)


def format_datetime_short(dt):
    return format_datetime(localtime(dt), format='n/j/y g:i A')
