from django.db import models

# Create your models here.

class ProveedorManager(models.Manager):
        pass
        

class Proveedor(models.Model):
        nombre     = models.CharField(max_length=150)
        correo     = models.CharField(max_length=150, blank=True)
        telefono   = models.CharField(max_length=150, blank=True)
        objects    = ProveedorManager()

        def __str__(self):
                return str(self.nombre)


