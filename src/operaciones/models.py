from django.db import models
from django.conf import settings
from django.db import DatabaseError, transaction
from django.core.files.images import ImageFile
from simple_history.models import HistoricalRecords
from PIL import Image, ImageOps
import random
import os
from proveedores.models import Proveedor
from items.models import Activo

User = settings.AUTH_USER_MODEL

# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name , ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=name, ext=ext)
    return "soportes_mantenimientos/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename)


MANTENIMIENTO_CHOICES = (
    ('correctivo','Correctivo'),
    ('preventivo','Preventivo'),
    ('compra','Compra')
    
)

class OperacionManager(models.Manager):
    def new(self,user,kwargs,soportes=None):
        try:
            with transaction.atomic():
                ## user validation done in view through session
                
                activoId = kwargs['activo_id']
                print(activoId)
                activos = Activo.objects.filter(pk=activoId)
                activo = activos[0]
                proveedorId = kwargs['proveedor']
                proveedores = Proveedor.objects.filter(pk=proveedorId)
                print(proveedorId)
                proveedor = proveedores[0]
                print('prefiltered dict ', kwargs)
                opfields = {key:value for key, value in kwargs.items() if key not in ['image','activo_id','csrfmiddlewaretoken']}
                print(opfields)
                #opfields = {k: kwargs[k] for k in k.keys() &  {'imagen','activo_id'}}
                #opfields = dict((k,kwargs[k]) for k not in ('imagen','activo_id'))

                ## limpiar dictionary

                filterDic = {}
                for key , value in opfields.items() :
                    filterDic[key] = value
                filterDic['activo'] = activo
                filterDic['proveedor'] = proveedor
                filterDic['user'] = user

                ## Creates and save
                #op = self.model.objects.create(**filterDic)

                op = Operacion(**filterDic)
                op.save()

                ##Create images

                for soporte in soportes:
                    soporte.operacion = op
                    soporte.save()
                

                print(op)
            return True
        except:
            print('error')
            return False
        
        
        
        # if kwargs.get('user'):
        #     user = kwargs.get('user')
        #     if user.is_authenticated():
        #         return self.model.objects.create(kwargs)
        # return None

class Operacion(models.Model):
    user          = models.ForeignKey(User)
    mantenimiento = models.CharField(max_length=50,default='correctivo',choices=MANTENIMIENTO_CHOICES)
    total         = models.DecimalField(default=0.00, max_digits=15,decimal_places=6)
    timestamp     = models.DateTimeField(auto_now_add=True)
    observacion   = models.TextField(blank=True)
    activo        = models.ForeignKey(Activo)
    proveedor     = models.ForeignKey(Proveedor, blank=True, null=True) 
    history       = HistoricalRecords()
    
    objects       = OperacionManager()   

    def __str__(self):
        return str(self.activo.descripcion) +"--" + str(self.activo.placa) + "--" + str(self.mantenimiento) + "--" + str(self.total) + "--" + str(self.timestamp) + "--" + self.hasSoporte()
    
    def getMantenimiento(self):
        return self.get_mantenimiento_display()

    def hasSoporte(self):
        if self.soportemantenimiento_set.count() > 0: 
            return "Tiene Soporte"
        else :
            return "Sin Soporte"
    
    def activo_name(self):
        return self.activo.descripcion

    def activo_placa(self):
        return self.activo.placa



class SoporteManager(models.Model):
    def new(self,**kwargs):
        print('create Soporte')

class SoporteMantenimiento(models.Model):
    image         = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    operacion     = models.ForeignKey(Operacion)
    history       = HistoricalRecords()

    def __str__(self):
        return  str(self.operacion.activo.descripcion) +"--" + str(self.operacion.activo.placa) + "--" + str(self.operacion.mantenimiento) + "--" + str(self.operacion.total) + "--" + str(self.operacion.timestamp)


