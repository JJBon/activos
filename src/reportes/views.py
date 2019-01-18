from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from utils.reports import genPivotHtml
#from django.contrib.auth import authenticate , login , get_user_model

# Create your views here.


def master_report(request):

    html = genPivotHtml()

    context = {
        "dataFrame": html
    }
    
    return render(request,"reportes/home.html",context)
