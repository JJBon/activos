from django.conf.urls import url


from .views import  SearchActivoView
    


urlpatterns = [
    url(r'^$', SearchActivoView.as_view(), name='query'),
    #url(r'^activos/(?P<pk>\d+)/$', ActivoDetailView.as_view()),
]