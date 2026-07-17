from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

# -----------------------------
# Load Model
# -----------------------------
model = pickle.load(open("Air_Quality_Model.pkl", "rb"))

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("UrbanAirPollutionDataset.csv")


# -----------------------------
# Graph Data
# -----------------------------

# AQI Trend (first 50 readings)
aqi_trend = df["AQI_Target"].head(50).tolist()

# Pollutant averages
pollutant_labels = [
    "PM2.5",
    "PM10",
    "NO",
    "SO",
    "CO",
    "O"
]

pollutant_values = [
    round(df["PM2.5"].mean(),2),
    round(df["PM10"].mean(),2),
    round(df["NO"].mean(),2),
    round(df["SO"].mean(),2),
    round(df["CO"].mean(),2),
    round(df["O"].mean(),2)
]

# AQI Categories

good = len(df[df["AQI_Target"] <= 50])

moderate = len(df[(df["AQI_Target"] > 50) & (df["AQI_Target"] <= 100)])

unhealthy = len(df[(df["AQI_Target"] > 100) & (df["AQI_Target"] <= 150)])

very_unhealthy = len(df[(df["AQI_Target"] > 150) & (df["AQI_Target"] <= 200)])

hazardous = len(df[df["AQI_Target"] > 200])



# -----------------------------
# Dashboard Statistics
# -----------------------------

average_aqi = round(df["AQI_Target"].mean(), 2)

maximum_aqi = round(df["AQI_Target"].max(), 2)

minimum_aqi = round(df["AQI_Target"].min(), 2)

good_days = len(df[df["AQI_Target"] <= 50])

moderate_days = len(df[(df["AQI_Target"] > 50) & (df["AQI_Target"] <= 100)])

poor_days = len(df[df["AQI_Target"] > 100])

# -----------------------------
# AQI Category
# -----------------------------

def get_category(aqi):

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Moderate"

    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"

    elif aqi <= 200:
        return "Unhealthy"

    elif aqi <= 300:
        return "Very Unhealthy"

    else:
        return "Hazardous"

# -----------------------------
# Health Recommendation
# -----------------------------

def get_health_advice(aqi):

    if aqi <= 50:
        return "Air quality is satisfactory."

    elif aqi <= 100:
        return "Sensitive people should reduce prolonged outdoor activity."

    elif aqi <= 150:
        return "Children and elderly should limit outdoor activity."

    elif aqi <= 200:
        return "Wear a mask when outdoors."

    elif aqi <= 300:
        return "Avoid outdoor activities."

    else:
        return "Stay indoors and avoid all outdoor exposure."

# -----------------------------
# Dashboard Route
# -----------------------------

@app.route("/")
def dashboard():

    return render_template(

        "dashboard.html",

        average_aqi=average_aqi,

        maximum_aqi=maximum_aqi,

        minimum_aqi=minimum_aqi,

        good_days=good_days,

        moderate_days=moderate_days,

        poor_days=poor_days,

    )


@app.route("/graph-data")
def graph_data():

    feature_importance = model.feature_importances_.tolist()

    feature_names = [
    "PM2.5",
    "PM10",
    "NO",
    "SO",
    "CO",
    "O",
    "Temp",
    "Humidity"
    ]

    return jsonify({

        "aqiTrend": aqi_trend,

        "pollutantLabels": pollutant_labels,

        "pollutantValues": pollutant_values,

        "categoryValues": [

            good,

            moderate,

            unhealthy,

            very_unhealthy,

            hazardous

        ],
        
        "featureImportance": feature_importance,
        "featureNames": feature_names

    })


# -----------------------------
# Prediction API
# -----------------------------

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    features = np.array([[
        float(data["PM2.5"]),
        float(data["PM10"]),
        float(data["NO"]),
        float(data["SO"]),
        float(data["CO"]),
        float(data["O"]),
        float(data["Temp_C"]),
        float(data["Humidity_%"])
    ]])

    prediction = float(model.predict(features)[0])

    category = get_category(prediction)

    advice = get_health_advice(prediction)

    return jsonify({

        "prediction": round(prediction,2),

        "category": category,

        "advice": advice

    })


# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)