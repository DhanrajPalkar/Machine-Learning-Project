
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

model = pickle.load(open('Air_Quality_Model.pkl', 'rb'))


df=pd.read_csv('air_quality_dataset_filled.csv')

def get_aqi_status(aqi):

    if 0 <= aqi <= 50:
        category = "Good 😊"
        message = ("Air quality is satisfactory and poses little "
                   "to no health risk.")

    elif 51 <= aqi <= 100:
        category = "Moderate 😐"
        message = ("Air quality is acceptable; however, a few sensitive "
                   "individuals may experience mild respiratory issues.")

    elif 101 <= aqi <= 150:
        category = "Unhealthy for Sensitive Groups 😷"
        message = ("People with respiratory conditions such as asthma "
                   "or heart disease are at greater risk.")

    elif 151 <= aqi <= 200:
        category = "Unhealthy ⚠️"
        message = ("Everyone may begin to experience adverse health "
                   "effects; sensitive groups may experience more serious "
                   "problems.")

    elif 201 <= aqi <= 300:
        category = "Very Unhealthy 🚨"
        message = ("Health warnings of emergency conditions. "
                   "The entire population is more likely to be affected.")

    else:
        category = "Hazardous ☠️"
        message = ("Health alert! Emergency conditions where the entire "
                   "population is likely to be impacted.")

    return category, message



@app.route('/')
def dashboard():

    return render_template(
        'index.html',
        prediction="",
        avg_aqi=round(df['AQI'].mean(),2),
        max_aqi=df['AQI'].max(),
        min_aqi=df['AQI'].min(),
        most_polluted=df.groupby('City')['AQI']
                            .mean()
                            .idxmax(),
        least_polluted=df.groupby('City')['AQI'].mean().idxmin()
    )



@app.route('/predict', methods=['POST'])
def predict():

    pm25 = float(request.form['pm25'])
    pm10 = float(request.form['pm10'])
    ozone = float(request.form['ozone'])
    no2 = float(request.form['no2'])
    co = float(request.form['co'])
    so2 = float(request.form['so2'])
    temperature = float(request.form['temperature'])
    humidity = float(request.form['humidity'])

    # Validate user inputs

    if not (0 <= pm25 <= 300):
        return "PM2.5 must be between 0 and 300"
    
    if not (0 <= pm10 <= 500):
        return "PM10 must be between 0 and 500"

    if not (0 <= ozone <= 800):
        return "Ozone must be between 0 and 800"

    if not (0 <= no2 <= 500):
        return "NO2 must be between 0 and 500"

    if not (0 <= co <= 500):
        return "CO must be between 0 and 500"

    if not (0 <= so2 <= 2000):
        return "SO2 must be between 0 and 2000"

    if not (0 <= humidity <= 100):
        return "Humidity must be between 0 and 100"

    features = [[pm25, pm10, ozone, no2,
                 co, so2, temperature, humidity]]

    predicted_aqi = round(model.predict(features)[0], 2)

    category, message = get_aqi_status(predicted_aqi)

    return render_template(
        'index.html',

        avg_aqi=round(df['AQI'].mean(),2),
        max_aqi=df['AQI'].max(),
        min_aqi=df['AQI'].min(),
        most_polluted=df.groupby('City')['AQI'].mean().idxmax(),
        least_polluted=df.groupby('City')['AQI'].mean().idxmin(),

        prediction=predicted_aqi,
        category=category,
        message=message
    )




if __name__ == '__main__':
    app.run(debug=True)

