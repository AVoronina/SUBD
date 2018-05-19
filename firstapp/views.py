from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import Top
from .models import Document
from .form import DocumentForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv
import codecs
from .result import read_file
from .result import predicts
from .result import get_date
from .result import get_fact_cost

def index(request):
    tops = Top.objects.all()
    return render(request, 'index.html', {'tops':tops})

def create(request):
    if request.method == 'POST':
        top = Top()
        top.top_name = request.POST.get('top_name')
        top.top_value = request.POST.get('top_value')
        top.save()
    return HttpResponseRedirect('/')

def delete(request, id):
    try:
        top = Top.objects.get(id=id)
        top.delete()
        return HttpResponseRedirect('/')
    except Top.DoesNotExist:
        return HttpResponseNotFound("<h2>Top not found</h2>")

def edit(request, id):
    try:
        top = Top.objects.get(id=id)

        if request.method == 'POST':
            top.top_name = request.POST.get('top_name')
            top.top_value = request.POST.get('top_value')
            top.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"top": top})
    except Top.DoesNotExist:
        return HttpResponseNotFound("<h2>Top not found</h2>")

def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        read_file(uploaded_file_url)
        predict_cost = predicts()
        output_date = get_date()
        fact_cost = get_fact_cost()
        print(predict_cost[0], output_date, fact_cost)
        return render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url
        })

    return render(request, 'index.html')
