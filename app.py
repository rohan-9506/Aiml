import pickle
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import logging

app = Flask(__name__)
model1 = pickle.load(open('productivity.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def index():
    return render_template('predict.html')

@app.route('/department')
def department():
    return render_template('department.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/data_predict', methods=['GET', 'POST'])
def predict():
    quarter = int(request.form['quarter'])
    department = request.form['department']

    if department.lower() == 'sewing':
        department = 1
    elif department.lower() == 'finishing':
        department = 0

    day = request.form['day']
    days = {'monday': 0, 'tuesday': 4, 'wednesday': 5, 'thursday': 3, 'saturday': 1, 'sunday': 2}
    day = days.get(day.lower())

    team_number = int(request.form['team_number'])
    time_allocated = int(request.form['time_allocated'])
    unfinished_items = int(request.form['unfinished_items'])
    over_time = int(request.form['overtime'])
    incentive = int(request.form['incentive'])
    idle_time = int(request.form['idle_time'])
    idle_men = int(request.form['idle_men'])
    style = int(request.form['no_of_style_change'])
    workers = int(request.form['no_of_workers'])

    prediction = model1.predict(pd.DataFrame([[quarter, department, day, team_number, time_allocated, unfinished_items, over_time, incentive, idle_time, idle_men, style, workers]], columns=['quarter', 'department', 'day', 'team_number', 'time_allocated', 'unfinished_items', 'over_time', 'incentive', 'idle_time', 'idle_men', 'style_change', 'no_of_workers']))
    logging.info(prediction)
    prediction = round(prediction.tolist()[0] * 100, 2)

    return render_template('productivity.html', y=prediction)

if __name__ == "__main__":
    app.run(debug=True)