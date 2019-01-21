
from django.conf.urls import url, include


from .views import  ActivoListView, ActivoDetailView,  ActivoDetailSlugView,update_home
from operaciones.views import (
     ActivoOperacionesView, 
     AddView, 
     add_operacion,
)

    


urlpatterns = [
    url(r'^$', ActivoListView.as_view(), name='list'),
    url(r'^update/$',update_home, name='update'),
    #url(r'^activos/(?P<pk>\d+)/$', ActivoDetailView.as_view()),
    url(r'^(?P<slug>[\w-]+)/$', ActivoDetailSlugView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/operaciones/$',ActivoOperacionesView.as_view(), name='operaciones'),
    #url(r'^(?P<slug>[\w-]+)/operaciones/', include("operaciones.urls", namespace='operaciones')),
    url(r'^(?P<slug>[\w-]+)/operaciones/nuevo$', AddView.as_view(), name='nuevo'),
    url(r'^(?P<slug>[\w-]+)/operaciones/add$',add_operacion,name='add')
]

