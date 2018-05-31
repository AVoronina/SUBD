from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv
import codecs
from .result import read_file, predicts_forest, predits_bayes, get_date, get_fact_cost, mean_absolute_err, get_crop, get_temp, get_test_data, get_train_data, get_tain_date, get_fact_cost_train
import matplotlib.pyplot as plt

def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        option = request.POST.get('option')
        read_file(uploaded_file_url)

        fact_cost = get_fact_cost()
        fact_cost = [float(item) for item in fact_cost]

        test_data = get_test_data()

        predict_cost1 = predicts_result(test_data, option)
        print(predict_cost1)
        output_date = get_date()
        err1 = mean_absolute_err(fact_cost, predict_cost1)
        graph(output_date, fact_cost, predict_cost1)

        train_data = get_train_data()
        predict_cost = predicts_result(train_data, option)

        train_date = get_tain_date()
        fact_train_cost = get_fact_cost_train()
        fact_train_cost = [float(item) for item in fact_train_cost]
        err = mean_absolute_err(fact_train_cost, predict_cost)
        graph_train_data(train_date, fact_train_cost, predict_cost)

        crop = get_crop()
        crop = [float(item) for item in crop]
        graph_crop(output_date, crop)
        temp = get_temp()
        temp = [float(item) for item in temp]
        graph_temp(output_date, temp)
        return render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url, 'option': option, 'err1': err1, 'err': err
        })

    return render(request, 'index.html')

def predicts_result(data, option):
    if option == '0':
        predict_cost = list(predicts_forest(data))
    else:
        predict_cost = list(predits_bayes(data))
        predict_cost = [float(item) for item in predict_cost]
    return predict_cost

def graph(X, Y1, Y2):
    line1, line2 = plt.plot(X, Y1, 'bD:', X, Y2, 'go:')
    plt.title(u'Прогнозирование цены')
    plt.xlabel(u'Дата')
    plt.ylabel(u'Стоимость')
    plt.xticks(rotation=45)
    plt.tick_params(axis='both', which='major', labelsize=7)
    plt.legend((line1, line2), (u'Рельная цена', u'Спрогнозированная цена'), loc = 'best')
    plt.grid()
    plt.savefig('D:/virtualenv/django/myenv/static/img/forecast.png', format = 'png')
    plt.clf()

def graph_crop(X, Y):
    line1 = plt.plot(X, Y, 'bD:')
    plt.title(u'Урожайность')
    plt.xlabel(u'Дата')
    plt.ylabel(u'Урожайность')
    plt.xticks(rotation=45)
    plt.tick_params(axis='both', which='major', labelsize=7)
    plt.legend((line1), (u'Урожайность'), loc = 'best')
    plt.grid()
    plt.savefig('D:/virtualenv/django/myenv/static/img/crop.png', format = 'png')
    plt.clf()

def graph_temp(X, Y):
    line1 = plt.plot(X, Y, 'bD:')
    plt.title(u'Температура')
    plt.xlabel(u'Дата')
    plt.ylabel(u'Температура')
    plt.xticks(rotation=45)
    plt.tick_params(axis='both', which='major', labelsize=7)
    plt.legend((line1), (u'Температура'), loc = 'best')
    plt.grid()
    plt.savefig('D:/virtualenv/django/myenv/static/img/temp.png', format = 'png')
    plt.clf()

def graph_train_data(X, Y1, Y2):
    line1, line2 = plt.plot(X, Y1, 'bD:', X, Y2, 'go:')
    plt.title(u'Прогнозирование цены')
    plt.xlabel(u'Дата')
    plt.ylabel(u'Стоимость')
    plt.xticks(rotation=45)
    plt.tick_params(axis='both', which='major', labelsize=7)
    plt.legend((line1, line2), (u'Рельная цена', u'Спрогнозированная цена'), loc = 'best')
    plt.grid()
    plt.savefig('D:/virtualenv/django/myenv/static/img/forecast1.png', format = 'png')
    plt.clf()
