import pandas as pd
import pickle
from sklearn.model_selection import train_test_split 
from sklearn.metrics import mean_absolute_error,r2_score
from xgboost import XGBRegressor

df=pd.read_csv('air_quality_dataset_filled.csv') 


df.drop_duplicates(inplace=True)


#AQI Prediction Model
x = df[["PM2.5", "PM10", "Ozone", "NO2", "CO", "SO2", "Temperature", "Humidity"]]

y=df["AQI"]

x_train,x_test,y_train,y_test=train_test_split(
    x,
    y,
    test_size =0.2,
    random_state=5
)


model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(x_train, y_train)

# predictions = model.predict(x_test)

# print("Mean Absolute Error:", mean_absolute_error(y_test, predictions))
# print("R2 Score:", r2_score(y_test, predictions))


pickle.dump(model, open('Air_Quality_Model.pkl', 'wb'))




# future prediction model
# df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# daily = df.groupby('Date')['AQI'].mean().reset_index()

# daily['Day'] = range(len(daily))

# x1 = daily[['Day']]
# y1 = daily['AQI']

# model = RandomForestRegressor()

# model.fit(x1, y1)

# pickle.dump(model, open('Future_AQI_Model.pkl', 'wb'))


