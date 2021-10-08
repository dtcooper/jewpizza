import subprocess


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip or "[unknown]"


try:
    GIT_REV = subprocess.check_output(['git', 'describe', '--tags', '--always', '--dirty'], text=True).strip()
except Exception:
    GIT_REV = 'unknown'
