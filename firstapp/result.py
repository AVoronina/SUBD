import csv
import codecs
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import mean_absolute_error

revenue = []
crop = []
temp = []
cost = []
cost_train = []
cost_test = []
x = []
x_train = []
x_test = []
date = []
date_output = []
crop_output = []
temp_output = []
date_train = []

def read_file(filename):
    x_train.clear()
    x.clear()
    x_test.clear()
    revenue.clear()
    crop.clear()
    temp.clear()
    cost.clear()
    cost_train.clear()
    cost_test.clear()
    date.clear()
    date_output.clear()
    crop_output.clear()
    temp_output.clear()
    date_train.clear()
    path = 'D:/virtualenv/django/myenv' + filename
    with codecs.open(path, 'r', 'utf-8') as file:
        reader = csv.reader(file, delimiter = ',')
        next(reader)
        for row in reader:
            date.append(row[0].strip())
            revenue.append(row[1].strip())
            crop.append(row[2].strip())
            temp.append(row[3].strip())
            cost.append(row[5].strip())
    index = 0
    while index < len(revenue) * 0.8:
        buf = []
        date_train.append(date[index])
        buf.append(revenue[index])
        buf.append(crop[index])
        buf.append(temp[index])
        buf = [float(item) for item in buf]
        x_train.append(buf)
        cost_train.append(cost[index])
        index += 1
    while index < len(revenue):
        buf = []
        date_output.append(date[index])
        crop_output.append(crop[index])
        temp_output.append(temp[index])
        buf.append(revenue[index])
        buf.append(crop[index])
        buf.append(temp[index])
        buf = [float(item) for item in buf]
        x_test.append(buf)
        cost_test.append(cost[index])
        index += 1

def predicts_forest(x_test):
    model =  RandomForestRegressor(n_estimators=500, oob_score=True, random_state=1)
    model.fit(x_train, cost_train)
    return model.predict(x_test)

def predits_bayes(x_test):
    model = GaussianNB()
    model = model.fit(x_train, cost_train)
    return model.predict(x_test)

def get_date():
    return date_output

def get_fact_cost():
    return cost_test

def mean_absolute_err(cost_test, predict_cost):
    return mean_absolute_error(cost_test, predict_cost)

def get_crop():
    return crop_output

def get_temp():
    return temp_output

def get_train_data():
    return x_train

def get_test_data():
    return x_test

def get_tain_date():
    return date_train

def get_fact_cost_train():
    return cost_train
