import csv
import codecs
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split

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
    while index < len(revenue) * 0.7:
        buf = []
        buf.append(revenue[index])
        buf.append(crop[index])
        buf.append(temp[index])
        x_train.append(buf)
        cost_train.append(cost[index])
        index += 1
    while index < len(revenue):
        buf = []
        date_output.append(date[index])
        buf.append(revenue[index])
        buf.append(crop[index])
        buf.append(temp[index])
        x_test.append(buf)
        cost_test.append(cost[index])
        index += 1
    # predicts()

def predicts():
    model =  RandomForestRegressor(n_estimators=10, oob_score=True, random_state=1)
    model.fit(x_train, cost_train)
    cost_output = model.predict(x_test)
    return model.predict(x_test)

def get_predict():
    print(cost_output)
    return cost_output
def get_date():
    return date_output
def get_fact_cost():
    return cost_test
