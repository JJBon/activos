from django.conf.urls import url, include

from .views import master_report

urlpatterns = [
    url(r'^$', master_report, name='home'),
]