from django.shortcuts import render
from django.views.generic import ListView , DetailView
from django.db.models import Q
from items.models import Activo
from items.forms import ActivoFilterForm

# Create your views here.

class SearchActivoView(ListView):
    template_name   = "search/view.html" 

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     return context

    ## need to send context to template

    def get_context_data(self,*args,**kwargs):
        context = super(SearchActivoView,self).get_context_data(*args,**kwargs)
        form = ActivoFilterForm()
        query = self.request.GET.get('q')
        context['form'] = form
        context['query'] = query
        return context

    def get_queryset(self,*args, **kwargs ):
        request = self.request

        print(type(request.GET))
        print(request.GET)
        
        if request.method == 'GET':

            method_dict = request.GET
            query = method_dict.get('q',None)

            if request.GET.getlist('filtros'):
                ## implement lazy loading
                return Activo.objects.parseChoices(request.GET.getlist('filtros'))
            
            if query:
                print('Query executed')
                print(query)
                return Activo.objects.search(query)


         
            
      
