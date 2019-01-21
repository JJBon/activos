import random
import os
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.db.models import Q
import datetime
# from model_utils import FieldTracker
from .utils import unique_slug_generator
from proveedores.models import Proveedor

# Create your models here.


ITEM_STATUS_CHOICES = (
    ('ok','OK'),
    ('seguimiento','SEGUIMIENTO'),
    ('revisión','REVISION'),
    ('fuera_de_servicio','FUERA DE SERVICIO'),
    ('cambio_placa','CAMBIO PLACA')
)

ITEM_PDV_CHOICES = (
    ('calle 104','CALLE 104'),
    ('calle 93','CALLE 93'),
    ('calle 72','CALLE 72')
)

ITEM_AREA_CHOICES = (
    ('bar','BAR'),
    ('baño','BAÑO'),
    ('bodega','BODEGA'),
    ('comedor','COMEDOR'),
    ('cuarto_de_aseo','CUARTO DE ASEO'),
    ('dulce','DULCE'),
    ('ensamble','ENSAMBLE'),
    ('granoleria','GRANOLERIA'),
    ('locker','LOCKER'),
    ('oficina','OFICINA'),
    ('panaderia','PANADERIA'),
    ('plancha','PLANCHA'),
    ('produccion','PRODUCCION'),
    ('punto','PUNTO'),
    ('stewart','STEWART'),
    ('sótano','SOTANO')
)

ITEM_TYPE_CHOICES = (
    ('equipo_hotel_rest','EQUIPO DE HOTELES Y RESTAURANTES'),
    ('muebles_oficina','MUEBLES ENSERES Y EQUIPO DE OFICINA'),
    ('computo_com','EQUIPO DE COMPUTO Y COMUNICACIONES'),
    ('instalaciones','INSTALACIONES ')
)

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name , ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "activos/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename)

# https://www.codingforentrepreneurs.com/blog/large-file-uploads-with-amazon-s3-django/

class ActivoManager(models.Manager):


    def create_activo(self,**kwargs):
        activo = self.create(**kwargs)
        return activo

    def enObservacion(self):
        return self.get_queryset().filter(enObservacion = True)
    
    def enRevision(self):
        return self.get_queryset().filter(estado = "revisión")
    
    def enSeguimiento(self):
        return self.get_queryset().filter(estado = "seguimiento")

    def fueraDeServicio(self):
        return self.get_queryset().filter(estado = "fuera_de_servicio")

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Activo.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None


    def getChoices(self, params = {'Estado':'estado','Pdv':'pdv','Ubicacion':'ubicacion'}):
       counter = 0
       groupChoices = []
       for groupName ,field in params.items():
           choices = []
           tuples = self.model._meta.get_field(field).choices
           for choice in tuples:
                label = choice[0]
                choices.append((counter,label))
                counter = counter + 1
           groupChoices.append((groupName,choices))
       return groupChoices

    def parseChoices(self,choices) :
        ## se optiene un array de numeros
        ## resultados de grupo tienen que estar en una tupla
        print("parse called")
        print(choices)
        ref = self.getChoices()
        print("ref called")
        print(ref)
        print(len(ref[0][1]),len(ref[1][1]),len(ref[2][1]))
        queryFilter = {}
        firstRange = len(ref[0][1])
        secondRange = firstRange + len(ref[1][1])

        for item in choices:
            group = 0
            value = None
            index = int(item)

            if index + 1 <= firstRange:
                group = 0
                print(ref[group][1][index][1])
                value = ref[group][1][index][1]
            elif index + 1 <= secondRange:
                group = 1
                value = ref[group][1][index-firstRange][1]
            else:
                group = 2
                print('index in array')
                print(index)
                print(firstRange)
                print(secondRange)
                print(firstRange + secondRange)
                print(index -(firstRange + secondRange))
                value = ref[group][1][index-secondRange][1]
            

            filterString = ref[group][0].lower()
            ##dictionary validation 
            if filterString not in queryFilter:
                queryFilter[filterString] = [value]
            else :
                queryFilter.get(filterString).append(value)
        print(queryFilter)
        #return queryFilter

        
        
        ## Or implementation
        # if 'estado' in queryFilter:
        #     list = self.filter(estado__in=queryFilter['estado'])
        #     finalList.extend(list)
        # if 'pdv' in queryFilter:
        #     list = self.filter(pdv__in=queryFilter['pdv'])
        #     finalList.extend(list)
        # if 'ubicacion' in queryFilter:
        #     list = self.filter(ubicacion__in=queryFilter['ubicacion'])
        #     finalList.extend(list)

        ## And implementation lazy loading involved , query executed when items called

        qs = None
        finalQ = None

        if queryFilter.get('estado'):
            finalQ = Q(estado__in=queryFilter.get('estado'))
        if queryFilter.get('pdv'):
            if finalQ is None:
                finalQ = Q(pdv__in=queryFilter.get('pdv'))
            else:
                finalQ = finalQ & Q(pdv__in=queryFilter.get('pdv'))
        if queryFilter.get('ubicacion'):
            if finalQ is None:
                finalQ = Q(ubicacion__in=queryFilter.get('ubicacion'))
            else:
                finalQ = finalQ & Q(ubicacion__in=queryFilter.get('ubicacion'))
            
        if finalQ:
            print('got finalQ')
            print(finalQ)
            return self.filter(finalQ)

        
    def search(self,query):
        lookups = Q(descripcion__icontains=query) | Q(pdv__icontains=query) |Q(estado__icontains=query)|   Q(placa__icontains=query) 
        return self.filter(lookups).distinct()

        

class Activo(models.Model):
    descripcion     = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True, unique=True) 
    estado          = models.CharField(max_length=120, default='ok', choices=ITEM_STATUS_CHOICES)
    enObservacion   = models.BooleanField(default=False)
    pdv             = models.CharField(max_length=120, default='104', choices=ITEM_PDV_CHOICES)
    ubicacion       = models.CharField(max_length=120, default='ok', choices=ITEM_AREA_CHOICES)
    proveedor       = models.ForeignKey(Proveedor, null=True, blank=True)
    marca           = models.CharField(max_length=120, blank=True)
    modelo          = models.CharField(max_length=120, blank=True)
    serie           = models.CharField(max_length=120, blank=True)
    placa           = models.CharField(max_length=120, blank=True)
    propio          = models.BooleanField(default=True)
    observaciones   = models.TextField(blank=True)
    vidautil        = models.IntegerField()
    image           = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    #price           = models.DecimalField(decimal_places=2,max_digits=20,default=39.99)
    timestamp       = models.DateTimeField(auto_now_add=True)

    @property
    def totalCost(self):
        _totalCost = self.gettotalCost()
        return _totalCost
    
    @property
    def totalPrevCost(self):
        _totalPrevCost = self.getPrevCost()
        return _totalPrevCost
    
    @property
    def totalCorCost(self):
        _totalCorCost = self.getCorCost()
        return _totalCorCost

    @property
    def num_cor(self):
        _num_cor = self.getCorCount()
        return _num_cor  

    @property
    def num_prev(self):
        _num_prev = self.getPrevCount()
        return _num_prev

    objects = ActivoManager()

    def operacionesWithDate(self,month=None,year=None):
        if month == None and year == None:
            operaciones     = self.operacion_set.all()
            operaciones     = [n for n in self.operacion_set.all() if n.mantenimiento != 'compra' ]
        else:
            operaciones     = [n for n in self.operacion_set.all() if datetime.datetime.date(n.timestamp).month == month and datetime.datetime.date(n.timestamp).year == year and n.mantenimiento != 'compra' ]
        return operaciones


    def gettotalCost(self,month=None,year=None):
        #instance = Activo.objects.get(slug=slug).operacion_set.all().order_by('-timestamp')
        operaciones     = self.operacionesWithDate(month,year)
        if operaciones == None:
            return 0
        costo = 0 
        for operacion in operaciones:
            if operacion.total == None:
                continue
            costo = costo + operacion.total
        return costo

    def getPrevCost(self,month=None,year=None):
        operaciones     = self.operacionesWithDate(month,year)
        if operaciones == None:
            return 0
        costo = 0
        for operacion in operaciones:
            if operacion.total == None:
                print("Null Cost")
                continue
            
            if operacion.mantenimiento == 'preventivo':
                costo = costo + operacion.total
                
        return costo 

    def getCorCost(self,month=None,year=None):
        operaciones     = self.operacionesWithDate(month,year)
        if operaciones == None:
            return 0
        costo = 0
        for operacion in operaciones:
            if operacion.total == None:
                print("Null Cost")
                continue
            
            if operacion.mantenimiento == 'correctivo':
                costo = costo + operacion.total
                
        return costo 

    def getCorCount(self,month=None,year=None):
        operaciones     = self.operacionesWithDate(month,year)
        if operaciones == None:
            return 0
        return len([op for op in operaciones if op.mantenimiento == 'correctivo' ]) 

    def getPrevCount(self,month=None,year=None):
        operaciones     = self.operacionesWithDate(month,year)
    
        if operaciones == None:
            return 0
        
        return len([op for op in operaciones if op.mantenimiento == 'preventivo' ])   




    def __str__(self):
        return self.descripcion + " : " + self.placa

    def get_absolute_url(self):
        #return "/activos/{slug}/".format(slug=self.slug)
        return reverse("activos:detail", kwargs={"slug":self.slug})
    
    def getEstado(self):
        return self.get_estado_display()

    def getImageUrl(self):
        if self.image and hasattr(self.image, 'url'):
            print('In image file',self.image.url)
            return self.image.url
        
        return None
     
    def getUbicacion(self):
        return self.get_ubicacion_display()

    def search(self,query):
        lookups = Q(descripcion__icontains=query) | Q(pdv__icontains=query) |Q(estado__icontains=query)
        return self.get_queryset().filter(lookups).distinct()
    
    def enAlerta(self):
        if self.estado != 'ok':
            return 'En Alerta'
        return 'Buen estado'

    

#    billing_profile     = models.ForeignKey(BillingProfile, null=True, blank=True)
#     order_id            = models.CharField(max_length=120 , blank=True)
#     shipping_address    = models.ForeignKey(Address, related_name="shipping_address", null=True, blank=True)
#     billing_address     = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True)
#     cart                = models.ForeignKey(Cart)
#     status              = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
#     shipping_total      = models.DecimalField(default=5.99, max_digits=100,decimal_places=2)
#     total               = models.DecimalField(default=0.00, max_digits=100,decimal_places=2)
#     active              = models.BooleanField(default=True)

# ORDER_STATUS_CHOICES = (
#     ('created','Created'),
#     ('paid','Paid'),
#     ('shipped','Shipped'),
#     ('refunded','Refunded')
# )

def activo_pre_save_receiver(sender, instance, *args, **kwargs):
    print("first save")
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if instance.estado != 'ok':
        print("check passed")
        instance.enObservacion = True
    else:
        print("check passed")
        instance.enObservacion = False    


pre_save.connect(activo_pre_save_receiver, sender=Activo)


