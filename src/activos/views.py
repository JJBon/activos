from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate , login , get_user_model
from django.views.generic import ListView 


from .forms import LoginForm
from items.models import Activo
# Class based viewed for homepage

class AlertSeguimientoView(ListView):
    template_name = "home_page.html"

    def get_queryset(self,*args,**kwargs):
        return Activo.objects.enSeguimiento()

class AlertRevisionView(ListView):
    template_name = "home_page.html"

    def get_queryset(self,*args,**kwargs):
        return Activo.objects.enRevision()

class FueraDeServicioView(ListView):
    template_name = "home_page.html"

    def get_queryset(self,*args,**kwargs):
        return Activo.objects.fueraDeServicio()

class HomePageView(ListView):
    template_name   = "home_page.html" 

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     return context

    def get_queryset(self,*args, **kwargs ):
        request = self.request
        return Activo.objects.enObservacion()

def home_page(request):
    return render(request,"home_page.html")

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    print("User auth status 1:")
    if form.is_valid():
        context['form'] = LoginForm()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        print("User auth status 2:")
        print(request.user.is_authenticated)
        if user is not None:
            print('user recognized')
            login(request, user)
            #context['form'] = LoginForm()
            return redirect("/login")
        else:
            print("Error")
    else:
        print('form not valid')

    return render(request, "auth/login.html", context)

def register_page(request):
    form = LoginForm()
    if form.is_valid():
        pass
    return render(request, "auth/login.html", {})