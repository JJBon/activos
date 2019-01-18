from django.shortcuts import render
from django.views.generic import ListView , DetailView
from django.http import Http404, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from items.models import Activo
from operaciones.forms import NewForm , SoporteForm
from .models import Operacion,SoporteMantenimiento
from django import forms

from django.shortcuts import render , redirect


# Create your views here.

class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class ActivoOperacionesView(ListView):
    #queryset        = Activo.objects.all()
    template_name   = "operaciones/home.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        activo = Activo.objects.get(slug=self.kwargs['slug'])
        context['activo'] = activo
        context['title'] = activo.descripcion
        context['slug'] = self.kwargs['slug']
        if activo.placa :
            context['placa'] = activo.placa
        return context

    def get_queryset(self, *args, **kwargs):

        request = self.request

        if request.method == 'GET':
            request = self.request
            slug    = self.kwargs.get('slug')
            #instance = get_object_or_404(Product, slug=slug, active=True)
            try:
                instance = Activo.objects.get(slug=slug).operacion_set.all().order_by('-timestamp')
            except Activo.DoesNotExist:
                raise Http404("Activo doesn't exist")
            except Activo.MultipleObjectsReturned:
                qs = Activo.objects.filter(slug=slug)
                instance = qs.first()
            return instance
        elif request.method == 'POST':
            print(request)
            return[]
        
        return []

def add_operacion(request, *args, **kwargs):
    print('add_operacion')
    if request.method == "POST":
        user = request.user
        activo_id = request.POST['activo_id']
        print('Post data :',request.POST )
        print('activoId: ',activo_id)
        activos = Activo.objects.filter(pk=activo_id)
        activo = activos[0]
      

        print('image should be here: ' , request.FILES)

        soportes = []

        for item in request.FILES.getlist('image'):
            print('image item', item)
            soporte = SoporteMantenimiento(image=item)
            soportes.append(soporte)
        
        form = SoporteForm(request.POST , request.FILES)
        if form.is_valid():
            print(form)
            print('form is valid')
            #form.save(commit=False)

        # fs = FileSystemStorage()
        # filename = fs.save(images.name, images)
        # uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)


        Operacion.objects.new(user,request.POST,soportes)

        next = request.POST.get('next','/activos/'+activo.slug+'/operaciones')
        print('redirect:',next)

        ## create operacion 



        return HttpResponseRedirect(next)
        #return render(request,"activos/"+activo.slug+"/operaciones")
        

class AddView(DetailView):
    template_name = "operaciones/new_op.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs)
        form = NewForm()
        object = kwargs['object']
        context['activo'] = object
        context['form'] = form
        context['img_form'] = SoporteForm()
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug    = self.kwargs.get('slug')
        print('nevera:',slug)
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Activo.objects.get(slug=slug)
        except Activo.DoesNotExist:
            raise Http404("Activo doesn't exist")
        except Activo.MultipleObjectsReturned:
            print(instance)
            qs = Activo.objects.filter(slug=slug)
            instance = qs.first()
        return instance






