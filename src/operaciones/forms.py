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
    
    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     proveedor = cleaned_data.get("proveedor")
    #     if proveedor == None:
    #         print("no proveedor")
    #         raise forms.ValidationError("Especificar proveedor")
    #     return cleaned_data
        
    
    def clean_proveedor(self):
        proveedor = self.cleaned_data.get("proveedor")
        if proveedor == None:
            print("no proveedor")
            raise forms.ValidationError("Especificar proveedor")
        return proveedor

class SoporteForm(ModelForm):
    class Meta:
        model = SoporteMantenimiento
        fields = ['image']
    
    def __init__(self, *args, **kwargs):
        super(SoporteForm,self).__init__(*args,**kwargs)
        self.fields['image'].widget.attrs.update({'type':'file','size':'50','accept':'image/*' ,'class':'form-control','multiple':True})
    
    # def clean_image(self):
    #     image = self.cleaned_data.get("image")
    #     print(image)
    #     print('should validate')
    #     if image == None:
    #         print('no image')
    #         try:
    #             raise forms.ValidationError("Especificar proveedor")
    #         except ValueError as e:
    #             print("in error")
    #             print(e)
    #     return image
