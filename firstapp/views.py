from django.shortcuts import render
from django.http import HttpResponse
# from .models import Document
# from .form import DocumentForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv
import codecs
from .result import read_file
from .result import predicts_forest, predits_bayes
from .result import get_date
from .result import get_fact_cost
import matplotlib.pyplot as plt

def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        option = request.POST.get('option')
        print(option)
        read_file(uploaded_file_url)
        if option == '0':
            predict_cost = list(predicts_forest())
        else:
            predict_cost = list(predits_bayes())
        output_date = get_date()
        fact_cost = get_fact_cost()
        fact_cost = [float(item) for item in fact_cost]
        graph(output_date, fact_cost, predict_cost, option)
        return render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url, 'option': option
        })

    return render(request, 'index.html')

def graph(X, Y1, Y2, option):
    line1, line2 = plt.plot(X, Y1, 'bD:', X, Y2, 'go:')
    plt.axis([1.0, 7.0, 0.0, 30.0])
    plt.title(u'Прогнозирование стоимости')
    plt.xlabel(u'Дата')
    plt.ylabel(u'Стоимость')
    plt.legend((line1, line2), (u'Рельная стоимость', u'Спрогнозированная стоимость'), loc = 'best')
    plt.grid()
    if option == '0':
        plt.savefig('D:/virtualenv/django/myenv/static/img/forecast1.png', format = 'png')
    else:
        plt.savefig('D:/virtualenv/django/myenv/static/img/forecast2.png', format = 'png')
    plt.clf()
