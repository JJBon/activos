from django import forms
from django.forms import ChoiceField
from .models import Activo

class ActivoFilterForm(forms.Form):
    selected = Activo.objects.getChoices(params = {'Estado':'estado','Pdv':'pdv','Ubicacion':'ubicacion'})
    filtros = ChoiceField(choices=selected,widget=forms.Select(attrs={'class':" selectpicker mb-2" ,'style':'width: auto', 'multiple':'multiple','data-live-search':'true'}))
