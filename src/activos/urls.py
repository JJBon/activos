
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from django.contrib import admin

# from items.views import ActivoListView, ActivoDetailView, ActivoDetailSlugView
from .views import home_page,HomePageView,AlertSeguimientoView,AlertRevisionView, FueraDeServicioView, login_page

urlpatterns = [
    #url(r'^$',home_page),
    url(r'^$',HomePageView.as_view(),name='home'),
    url(r'^seguimiento/$',AlertSeguimientoView.as_view(),name='seguimiento'),
    url(r'^revision/$',AlertRevisionView.as_view(),name='revision'),
    url(r'^fueraDeServicio/$',FueraDeServicioView.as_view(),name='fueraDeServicio'),
    # url(r'^activos/$', ActivoListView.as_view()),
    # url(r'^activos/(?P<pk>\d+)/$', ActivoDetailView.as_view()),
    # url(r'^activos/(?P<slug>[\w-]+)/$', ActivoDetailSlugView.as_view()),

    ## extend//include urls to another path
    url(r'^activos/', include("items.urls", namespace='activos')),
    url(r'^search/', include("search.urls", namespace='search')),
    url(r'^reportes/', include("reportes.urls", namespace='reportes')),
    url(r'^login/$', login_page, name='login'),
    url(r'^admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

