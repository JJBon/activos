from django.http import Http404
from django.views.generic import ListView , DetailView
from django.shortcuts import render, get_object_or_404


from .models import Activo
from .forms import ActivoFilterForm

# Create your views here.


class ActivoListView(ListView):
    template_name   = "items/list.html" 

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     return context

    ## need to send context to template

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        form = ActivoFilterForm()
        context['form'] = form
        return context

    def get_queryset(self,*args, **kwargs ):
        request = self.request

        print(type(request.GET))
        print(request.GET)
        
        if request.method == 'GET':
            if request.GET.getlist('filtros'):
                ## implement lazy loading
                return Activo.objects.parseChoices(request.GET.getlist('filtros'))


            if not request.GET:
                print("no variables")
                return Activo.objects.all()
            
        return []

class ActivoDetailSlugView(DetailView):
    #queryset        = Activo.objects.all()
    template_name   = "items/detail.html"

    def get_object(self, *args, **kwargs):
        request = self.request
        slug    = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Activo.objects.get(slug=slug)
        except Activo.DoesNotExist:
            raise Http404("Activo doesn't exist")
        except Activo.MultipleObjectsReturned:
            qs = Activo.objects.filter(slug=slug)
            instance = qs.first()
        return instance

class ActivoDetailView(DetailView):
    #queryset        = Activo.objects.all() no hay necesidad por get_object
    template_name   = "items/detail.html" 
    
    def get_context_data(self,*args,**kwargs):
        context = super(ActivoDetailView,self).get_context_data(*args,**kwargs)
        print(context)
        return context

    # def get_object(self, *args, **kwargs):
    #     request = self.request
    #     pk      = self.kwargs.get('pk')
    #     instance = Activo.objects.get_by_id(pk)
    #     if instance is None:
    #         raise Http404("Activo doesn't exist")
    #     return instance

    def get_queryset(self,*args, **kwargs ):
        print('Retrieving')
        request = self.request
        print(request)
        pk      = self.kwargs.get('pk')
        return Activo.objects.filter(pk=pk)