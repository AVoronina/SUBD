import csv
import codecs
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.naive_bayes import GaussianNB

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
cost_output = []

def read_file(filename):
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
    cost_output = []
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
        buf.append(revenue[index])
        buf.append(crop[index])
        buf.append(temp[index])
        buf = [float(item) for item in buf]
        x_test.append(buf)
        cost_test.append(cost[index])
        index += 1

def predicts_forest():
    model =  RandomForestRegressor(n_estimators=500, oob_score=True, n_jobs=-1, random_state=1)
    model.fit(x_train, cost_train)
    return model.predict(x_test)

def predits_bayes():
    model = GaussianNB()
    model = model.fit(x_train, cost_train)
    return model.predict(x_test)

def get_date():
    return date_output
def get_fact_cost():
    return cost_test
