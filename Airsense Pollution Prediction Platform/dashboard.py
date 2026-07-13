import pandas as pd
import matplotlib.pyplot as plt
import pickle

model = pickle.load(open('Future_AQI_Model.pkl', 'rb'))

df=pd.read_csv('air_quality_dataset_filled.csv')

df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

daily_aqi = df.groupby('Date')['AQI'].mean()

plt.figure(figsize=(12,5))
plt.plot(daily_aqi.index, daily_aqi.values)

plt.title('Average AQI Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Average AQI')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('static/aqi_trend.png')


city_aqi = df.groupby('City')['AQI'].mean().sort_values(ascending=False)

plt.figure(figsize=(12,6))
city_aqi.head(10).plot(kind='bar')

plt.title('Top 10 Most Polluted Cities')
plt.ylabel('Average AQI')

plt.tight_layout()
plt.savefig('static/city_comparison.png')


daily = df.groupby('Date')['AQI'].mean().reset_index()

daily['Day'] = range(len(daily))


future_days = list(range(len(daily), len(daily)+30))

future_pred = model.predict(
    pd.DataFrame(future_days, columns=['Day'])
)



plt.figure(figsize=(12,5))

plt.plot(daily['Day'], daily['AQI'],
         label='Historical AQI')

plt.plot(future_days, future_pred,
         label='Future AQI Prediction')

plt.legend()

plt.title('Future Air Pollution Prediction')

plt.savefig('static/future_prediction.png')