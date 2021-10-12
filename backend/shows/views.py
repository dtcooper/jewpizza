import json
import itertools

from django.core import serializers
from django.views.generic import TemplateView, View
from django.http import JsonResponse

from .models import Show, ShowDate


class ShowsMasterListView(TemplateView):
    template_name = "shows/shows_master_list.html"
    extra_context = {"title": "Shows"}


class DevExportView(View):
    models_to_serialize = (Show, ShowDate)

    def get(self, request, *args, **kwargs):
        all_objects = itertools.chain.from_iterable(model.objects.all() for model in self.models_to_serialize)
        data = json.loads(serializers.serialize('json', all_objects))
        return JsonResponse(data, safe=False)
