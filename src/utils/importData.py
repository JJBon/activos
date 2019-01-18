
import pandas as pd
from django.db import DatabaseError, transaction
from items import models as activoM 
from proveedores.models import Proveedor
from operaciones.models import MANTENIMIENTO_CHOICES, Operacion
from django.contrib.auth.models import User



def choiceHelper(x,choices,default):

    # y choices
    for choice in choices:
        #print(x[0:3].lower(),' : ',choice[0].lower())

        if x[0:2].lower() in choice[0].lower() :
            return choice[0]
    
    return default

def localHelper(x,choices):
    for choice in choices:
        print(x.lower(),' : ',choice[0].lower())

        if x.lower() in choice[0].lower() :
            return choice[0]


def inRevision(x):
    if x != 'ok':
        return True
    return False

def isOwned(x):
    if x == 'PROPIA':
        return True
    return False

## ciclo para insertar Activos usando el orm de django

activosFrame  = pd.read_excel('/Users/juanjosebonilla/Desktop/Sistemas/WebProjects/activos/src/utils/TablasSql.xlsx',sheet_name='activos')
operacionesFrame  = pd.read_excel('/Users/juanjosebonilla/Desktop/Sistemas/WebProjects/activos/src/utils/TablasSql.xlsx',sheet_name='operaciones')

@transaction.atomic
def saveActivos():

    try:


            # nombre     = models.CharField(max_length=150)
            # correo     = models.CharField(max_length=150, blank=True)
            # telefono   = models.CharField(max_length=150, blank=True)
            # objects    = ProveedorManager()



            
            activosFrame['vidaUtil'] = activosFrame['vidaUtil'].fillna(0)
            #activosFrame['vidaUtil'] = activosFrame['vidaUtil'].astype(int)
            print(activosFrame)

            operacionesFrame  = pd.read_excel('/Users/juanjosebonilla/Desktop/Sistemas/WebProjects/activos/src/utils/TablasSql.xlsx',sheet_name='operaciones')
            print(operacionesFrame)

            operaciones = []

            for index, row in activosFrame.iterrows():

                # descripcion     = models.CharField(max_length=120)
                # slug            = models.SlugField(blank=True, unique=True) 
                # estado          = models.CharField(max_length=120, default='ok', choices=ITEM_STATUS_CHOICES)
                # enObservacion   = models.BooleanField(default=False)
                # pdv             = models.CharField(max_length=120, default='104', choices=ITEM_PDV_CHOICES)
                # ubicacion       = models.CharField(max_length=120, default='ok', choices=ITEM_AREA_CHOICES)
                # proveedor       = models.ForeignKey(Proveedor, null=True, blank=True)
                # marca           = models.CharField(max_length=120, blank=True)
                # modelo          = models.CharField(max_length=120, blank=True)
                # serie           = models.CharField(max_length=120, blank=True)
                # placa           = models.CharField(max_length=120, blank=True)
                # propio          = models.BooleanField(default=True)
                # observaciones   = models.TextField(blank=True)
                # vidautil        = models.IntegerField()
                # image           = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
                #price           = models.DecimalField(decimal_places=2,max_digits=20,default=39.99)

                # objects = ActivoManager()

                #image           = models.ImageField(upload_to=upload_image_path,null=True,blank=True)
                #featured =      models.BooleanField(default=False)
                # timestamp       = models.DateTimeField(auto_now_add=True)

                estadoChoice = choiceHelper(row['estado'],activoM.ITEM_STATUS_CHOICES,None)
                pdvChoice = localHelper(row['local'],activoM.ITEM_PDV_CHOICES)
                areaChoice = choiceHelper(row['ubicacion2'],activoM.ITEM_AREA_CHOICES,'comedor')

                revBool = inRevision(estadoChoice) 


                fields = {'descripcion':row['nombre'],'estado':estadoChoice,'enObservacion':revBool,'pdv':pdvChoice,'ubicacion':areaChoice,
                        'proveedor':None,'marca':row['marca'],'modelo':row['modelo'],'serie':row['serie'],'placa':row['placa'],'propio':isOwned(row['activoPropio']),
                        'vidautil':int(row['vidaUtil'])
                        #'vidautil':float(row['vidaUtil'] if row['vidaUtil'] != None else None )
                }

                activo = activoM.Activo(**fields)
                activo.save()

                ## Agregar operaciones 

                opActivoFr = operacionesFrame[operacionesFrame['activo_id'] == row['id']]

                # user          = models.ForeignKey(User)
                # mantenimiento = models.CharField(max_length=50,default='correctivo',choices=MANTENIMIENTO_CHOICES)
                # total         = models.DecimalField(default=0.00, max_digits=15,decimal_places=6)
                # timestamp     = models.DateTimeField(auto_now_add=True)
                # observacion   = models.TextField(blank=True)
                # activo        = models.ForeignKey(Activo)
                # proveedor     = models.ForeignKey(Proveedor) 
                # history       = HistoricalRecords()
                
                # objects       = OperacionManager()   


                if len(opActivoFr.index) > 0:
                    for index2, row2 in opActivoFr.iterrows():
                        # query proveedor
                        fields = {'mantenimiento':choiceHelper(row2['tipoOperacion'],MANTENIMIENTO_CHOICES,'correctivo'),'total':row2['costo'],'observacion':row2['descripción']}
                        op = Operacion(**fields)

                        provName = row2['proveedor']
                        if (provName != None) and (provName != "") :
                            proveedores = Proveedor.objects.filter(nombre = provName)
                            if len(proveedores) > 0:
                                proveedor = proveedores[0]
                                op.proveedor = proveedor
                        user = User.objects.filter(username = 'juanjosebonilla')[0]
                        op.user = user

                        op.activo = activo    
                        op.timestamp = row2['fecha']
                        operaciones.append(op)
            operaciones.sort(key=lambda x: x.timestamp,reverse = False)
            print(operaciones)
            for operacion in operaciones:
                overDate = operacion.timestamp
                print(overDate)
                operacion.save()
                operacion.timestamp = overDate
                operacion.save()
      

    except DatabaseError as e:
        message = 'Database Error: ' + str(e.message)

def saveProveedores():
    proveedores = operacionesFrame['proveedor'].unique()

    for prov in proveedores:
        proveedor = Proveedor(nombre = prov)
        proveedor.save()

 



saveProveedores()
saveActivos()

