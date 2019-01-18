from django.forms import ModelForm
from django import forms
from operaciones.models import Operacion, SoporteMantenimiento

class NewForm(ModelForm):
    class Meta:
        model = Operacion
        fields = ['mantenimiento','proveedor','total','observacion']
    
    def __init__(self, *args, **kwargs):
        super(NewForm,self).__init__(*args,**kwargs)
        self.fields['mantenimiento'].widget.attrs.update({'class':'form-control'})
        self.fields['total'].widget.attrs.update({'class':'form-control'})
        self.fields['observacion'].widget.attrs.update({'class':'form-control'})
        self.fields['proveedor'].widget.attrs.update({'class':'form-control'})

class SoporteForm(ModelForm):
    class Meta:
        model = SoporteMantenimiento
        fields = ['image']
    
    def __init__(self, *args, **kwargs):
        super(SoporteForm,self).__init__(*args,**kwargs)
        self.fields['image'].widget.attrs.update({'type':'file','size':'50','accept':'image/*' ,'class':'form-control','multiple':True})