from django.conf import settings
from django.http.request import split_domain_port
from django.http import HttpResponse, HttpResponseForbidden


def server_logs(request):
    if request.user.is_superuser:
        return HttpResponse(headers={"X-Accel-Redirect": f"/__internal__{request.get_full_path()}"})
    else:
        return HttpResponseForbidden()
