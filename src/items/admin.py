from django.contrib import admin

# Register your models here.

from django.db.models import Q
from .models import Activo


# ITEM_STATUS_CHOICES = (
#     ('ok','OK'),
#     ('seguimiento','SEGUIMIENTO'),
#     ('revisión','REVISION'),
#     ('fuera_de_servicio','FUERA DE SERVICIO'),
#     ('cambio_placa','CAMBIO PLACA')
# )

ITEM_STATUS_CHOICES = (
    ('enAlerta','EN ALERTA'),
    ('ok','OK'),
)


class EstadoListFilter(admin.SimpleListFilter):
    title = 'En Alerta'
    parameter_name = 'estado_category'

    def lookups(self,request,model_admin):
        return ITEM_STATUS_CHOICES
    
    def queryset(self, request , queryset):
        if self.value() == 'enAlerta':
            return queryset.filter(
                Q(estado='seguimiento') | Q(estado='revisión') | Q(estado='fuera_de_servicio') | Q(estado='cambio_placa')
            )

class ActivoAdmin(admin.ModelAdmin):

    search_fields = ('placa','descripcion')

    list_display = ['descripcion','placa','ubicacion','estado']
    #list_display = ['__str__','slug']

    list_filter = ('pdv','estado', EstadoListFilter,'ubicacion')

    class Meta:
        model = Activo

admin.site.register(Activo, ActivoAdmin)