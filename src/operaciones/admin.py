from django.contrib import admin
from django.db.models import Q , Count
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.

from .models import Operacion, SoporteMantenimiento


# class EstadoListFilter(admin.SimpleListFilter):
#     title = 'En Alerta'
#     parameter_name = 'estado_category'

#     def lookups(self,request,model_admin):
#         return ITEM_STATUS_CHOICES
    
#     def queryset(self, request , queryset):
#         if self.value() == 'enAlerta':
#             return queryset.filter(
#                 Q(estado='seguimiento') | Q(estado='revisión') | Q(estado='fuera_de_servicio') | Q(estado='cambio_placa')

class sinSoporteFilter(admin.SimpleListFilter):
    title = 'Sin Soporte'
    parameter_name = 'soporte'

    def lookups(self, request, model_admin):
        return (
            ('True','Con Soporte'),
            ('False','Sin Soporte')
        )
    def queryset(self, request, queryset):
        if self.value() == 'False':
            return queryset.annotate(soportemantenimientos_num=Count('soportemantenimiento')).filter(soportemantenimientos_num=0)
        if self.value() == 'True':
            return queryset.annotate(soportemantenimientos_num=Count('soportemantenimiento')).filter(soportemantenimientos_num__gt=0)




class OperacionAdmin(SimpleHistoryAdmin):

    

    list_display = ['timestamp','total','mantenimiento','activo_name','activo_placa']
    #list_display = ['__str__','slug']
    list_filter = ('mantenimiento','activo__pdv',sinSoporteFilter)

    class Meta:
        model = Operacion

# admin.site.register(Activo, ActivoAdmin)

admin.site.register(Operacion,OperacionAdmin)
admin.site.register(SoporteMantenimiento,SimpleHistoryAdmin)


