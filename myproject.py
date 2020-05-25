from flask import Flask
from flask import jsonify
from flask import request
import pandas as pd
from flask import Flask, render_template
import requests
import csv
import json
from pymongo import MongoClient
import uuid  # UUIDs for documents
import random  # to randomly generate doc data
import pandas as pd
import json
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from io import BytesIO
import matplotlib

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


mongo_client = MongoClient('localhost', 27017)
db = mongo_client.testzomato
kothruddb = db.kothrud
aundhdb = db.aundh
parvatidb = db.parvati


app = Flask(__name__)

@app.route('/')
def hello(name=None):
    return render_template('login.html')

database={'admin':'1234'}

@app.route('/zomato',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
	    return render_template('login.html',info='Invalid User')
    else:
        if database[name1]!=pwd:
            return render_template('login.html',info='Invalid Password')
        else:
	        return render_template('index.html')


@app.route('/ml/prediction', methods=['GET','POST'])
def mlprediction():
    # {
	# "first":10 ,
	# "second":10,
	# "third":10,
	# "fourth":10
    #  }
    
    data = request.get_json(force=True)
    print(data)
    data1 = data['first']
    data2 = data['second']
    data3 = data['third']
    data4 = data['fourth']
    data5 = data['fifth']

    resultadd = int(data3) + int(data4) +int(data5)
    # rlist = func(datav)
    # df = pd.io.json.json_normalize(rlist)
    # menuitems=df['cuisines']
    # print(menuitems)
    # data = request.get_json(force=True)
    # val1=data['value']
    # dataset = pd.read_csv('/home/wideeye/Pictures/jango/Linear Regression/Salary_Data.csv')
    # X = dataset.iloc[:, :-1].values
    # y = dataset.iloc[:, 1].values

    # from sklearn.model_selection import train_test_split
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

    # from sklearn.linear_model import LinearRegression
    # regressor = LinearRegression()
    # regressor.fit(X_train, y_train)

    # predicted_salary = int(regressor.predict([[int(val1)]]))

    return jsonify({'result': resultadd})


# def loaddatafunc(col_name,nearby_restaurants):
#     mongo_client = MongoClient('localhost', 27017)
#     db = mongo_client.testzomato[col_name]
#     ressult=db.insert_many(nearby_restaurants)


@app.route('/ml/loaddata', methods=['POST'])
def getdata():
    data = request.get_json(force=True)
    datav = data['value']
    aundh = {"18.5602": "73.8031"}
    kothrud = {"18.4949": "73.8441"}
    parvati = {"18.4949": "73.8441"}
    shivajinagar = {"18.5314 : 73.8446"}
    if datav == "kothrud":
        geoList = [kothrud]
    if datav == "aundh":
        geoList = [aundh]
    if datav == "parvati":
        geoList = [parvati]
    if datav == "shivajinagar":
        geoList = [shivajinagar]
    nearby_restaurants = []
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json",
              "user_key": "cb4e85bf9a21ce81d81f16062f44c948"}

    for i in geoList:
        for key, value in i.items():
            r = (requests.get("https://developers.zomato.com/api/v2.1/geocode?lat=" + key + "&lon=" + value,
                              headers=header).content).decode("utf-8")
            a = json.loads(r)
            for nearby_restaurant in a['nearby_restaurants']:
                nearby_restaurants.append({"name": nearby_restaurant['restaurant']['name'],
                                           "location": nearby_restaurant['restaurant']['location']['locality'],
                                           "cuisines": nearby_restaurant['restaurant']['cuisines'],
                                           "average_cost_for_two": nearby_restaurant['restaurant'][
                    'average_cost_for_two'],
                    "has_table_booking": nearby_restaurant['restaurant']['has_table_booking'],
                    "has_online_delivery": nearby_restaurant['restaurant'][
                    'has_online_delivery'],
                    "is_delivering_now": nearby_restaurant['restaurant']['is_delivering_now'],
                    "aggregate_rating": nearby_restaurant['restaurant']['user_rating'][
                    'aggregate_rating'],
                    "rating_text": nearby_restaurant['restaurant']['user_rating'][
                    'rating_text']})
    if datav == "kothrud":
        try:
            result = kothruddb.insert_many(nearby_restaurants)
        except Exception as e:
            print("error")
    if datav == "aundh":
        try:
            result = aundhdb.insert_many(nearby_restaurants)
        except Exception as e:
            print("error")
    if datav == "parvati":
        try:
            result = parvatidb.insert_many(nearby_restaurants)
        except Exception as e:
            print("error")

    return json.dumps(nearby_restaurants, default=str)


# def func(db_name):
#     response = db_name.find({}, {"_id": 0, "name": 0, "location": 0, "aggregate_rating": 0,
#                                  "rating_text": 0, "average_cost_for_two": 0})
#     return response

def func(col_name):
    mongo_client = MongoClient('localhost', 27017)
    db = mongo_client.testzomato[col_name]
    listt = db.find({}, {"_id": 0, "name": 0, "location": 0, "aggregate_rating": 0,
                         "rating_text": 0, "average_cost_for_two": 0})
    menulist = list(listt)

    return menulist


def menuitem(col_name):
    mongo_client = MongoClient('localhost', 27017)
    db = mongo_client.testzomato[col_name]
    listt = db.find({}, {'cuisines': 1, "_id": 0})
    menulist = list(listt)

    return menuitems

def prediction(col_name):
    mongo_client = MongoClient('localhost', 27017)
    db = mongo_client.testzomato[col_name]
    listt = db.find({}, {"_id": 0, "name": 0, "location": 0, "aggregate_rating": 0,
                         "rating_text": 0, "average_cost_for_two": 0})
    menulist = list(listt)

    return menulist


@app.route('/ml/famousmenu/<location>', methods=['GET'])
def hotelsmenus(location):
    
    location = location
    menulist = func(location)
    cuisines = []
    for i in menulist:
        cuisines.append(i['cuisines'])
    listt = []
    splitlist = []
    for i in cuisines:
        splitlist.append(i.split(","))
    for i in splitlist:
        for j in i:
            listt.append(j.strip())
    counts = dict()
    for word in listt:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1  
            
    plt.barh(range(len(counts)), list(counts.values()), align='center')
    plt.yticks(range(len(counts)), list(counts.keys()))
    plt.xticks([])
    
    #plt.show()
    figfile = BytesIO()
    plt.savefig(figfile, format='png')

    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(figfile.getvalue()).decode('utf8')    
    
    #return jsonify({'img': pngImageB64String})
    plt.close('all')
    return render_template("hello.html", image=pngImageB64String)
    
    #return {"data": counts}

@app.route('/ml/onlinedelivery/<location>', methods=['GET'])
def onlinedelivery(location):
    
    location = location
    rlist = func(location)
    onlineDeliveryyes = 0
    onlineDeliveryno = 0

    for i in rlist:
        if i['has_online_delivery'] == 1:
            onlineDeliveryyes = onlineDeliveryyes + 1
        if i['has_online_delivery'] == 0:
            onlineDeliveryno = onlineDeliveryno+1 
    
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'No', 'Yes'
    sizes = [onlineDeliveryno,onlineDeliveryyes]
    explode = (0.2,0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=30)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    #plt.show()

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig1).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')    
    
    #return jsonify({'img': pngImageB64String})
    return render_template("hello.html", image=pngImageB64String)


@app.route('/ml/tablebooking/<location>', methods=['GET'])
def tablebooking(location):
    location = location
    rlist = func(location)
    tableBookingyes = 0
    tableBookingno = 0

    for i in rlist:
        if i['has_table_booking'] == 1:
            tableBookingyes = tableBookingyes + 1
        if i['has_table_booking'] == 0:
            tableBookingno = tableBookingno+1 
    

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'No', 'Yes'
    sizes = [tableBookingno,tableBookingyes]
    explode = (0.2,0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=30)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    #plt.show()

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig1).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')    
    
    #return jsonify({'img': pngImageB64String})
    
    return render_template("hello.html", image=pngImageB64String)   

@app.route('/ml/deliveringnow/<location>', methods=['GET'])
def deliveringnow(location):
    location = location
    rlist = func(location)
    deliveringNowyes = 0
    deliveringNowno = 0

    for i in rlist:
        if i['is_delivering_now'] == 1:
            deliveringNowyes = deliveringNowyes + 1
        if i['is_delivering_now'] == 0:
            deliveringNowno = deliveringNowno+1 
    
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'No', 'Yes'
    sizes = [deliveringNowno,deliveringNowyes]
    explode = (0.2,0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=30)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    #plt.show()

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig1).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')    
    
    #return jsonify({'img': pngImageB64String})
    
    return render_template("hello.html", image=pngImageB64String) 


    #return {"data": [deliveringNowyes,deliveringNowno]}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
