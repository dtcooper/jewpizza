from django.urls import path
from django.views.generic import TemplateView


app_name = 'webcore'
urlpatterns = [
    path('', TemplateView.as_view(template_name='webcore/index.html',
                                  extra_context={'title': 'jew.pizza Demo Site'}), name='index'),
]
