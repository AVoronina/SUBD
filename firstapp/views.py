from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv
import codecs
from .result import read_file, predicts_forest, predits_bayes, get_date, get_fact_cost, mean_absolute_err, get_crop, get_temp
import matplotlib.pyplot as plt

def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        option = request.POST.get('option')
        read_file(uploaded_file_url)
        if option == '0':
            predict_cost = list(predicts_forest())
        else:
            predict_cost = list(predits_bayes())
            predict_cost = [float(item) for item in predict_cost]
        output_date = get_date()
        fact_cost = get_fact_cost()
        fact_cost = [float(item) for item in fact_cost]
        err = mean_absolute_err(fact_cost, predict_cost)
        graph(output_date, fact_cost, predict_cost, option)
        crop = get_crop()
        crop = [float(item) for item in crop]
        graph_crop(output_date, crop)
        temp = get_temp()
        temp = [float(item) for item in temp]
        graph_temp(output_date, temp)
        return render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url, 'option': option, 'err': err
        })

    return render(request, 'index.html')

def graph(X, Y1, Y2, option):
    line1, line2 = plt.plot(X, Y1, 'bD:', X, Y2, 'go:')
    plt.axis([1.0, 7.0, 0.0, 30.0])
    plt.title(u'Прогнозирование цены')
    plt.xlabel(u'Дата')
    plt.ylabel(u'Стоимость')
    plt.legend((line1, line2), (u'Рельная цена', u'Спрогнозированная цена'), loc = 'best')
    plt.grid()
    plt.savefig('D:/virtualenv/django/myenv/static/img/forecast.png', format = 'png')
    plt.clf()
def graph_crop(X, Y):
    line1 = plt.plot(X, Y, 'bD:')
    plt.axis([1.0, 7.0, 15.0, 40.0])
    plt.title(u'Урожайность')
    plt.xlabel(u'Дата')
    plt.ylabel(u'Урожайность')
    plt.legend((line1), (u'Урожайность'), loc = 'best')
    plt.grid()
    plt.savefig('D:/virtualenv/django/myenv/static/img/crop.png', format = 'png')
    plt.clf()
def graph_temp(X, Y):
    line1 = plt.plot(X, Y, 'bD:')
    plt.axis([1.0, 7.0, -10.0, 30.0])
    plt.title(u'Температура')
    plt.xlabel(u'Дата')
    plt.ylabel(u'Температура')
    plt.legend((line1), (u'Температура'), loc = 'best')
    plt.grid()
    plt.savefig('D:/virtualenv/django/myenv/static/img/temp.png', format = 'png')
    plt.clf()
