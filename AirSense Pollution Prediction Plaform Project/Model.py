import pandas as pd
import pickle
from sklearn.model_selection import train_test_split 
# from sklearn.metrics import mean_absolute_error,r2_score
from xgboost import XGBRegressor
# from sklearn.metrics import mean_squared_error
# import numpy as np

df = pd.read_csv('UrbanAirPollutionDataset.csv')



x = df[['PM2.5','PM10','NO','SO','CO','O','Temp_C','Humidity_%']]

y = df['AQI_Target']



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

pickle.dump(model, open('Air_Quality_Model.pkl', 'wb'))

# predictions = model.predict(x_test)

# print("Mean Absolute Error:", mean_absolute_error(y_test, predictions))
# print("R2 Score:", r2_score(y_test, predictions))


# rmse = np.sqrt(mean_squared_error(y_test, predictions))
# print("RMSE:", rmse)

# comparison = pd.DataFrame({
#     "Actual": y_test.values,
#     "Predicted": predictions
# })

# print(comparison.sample(10))

# train_predictions = model.predict(x_train)
# test_predictions = model.predict(x_test)

# print("Train R2 :", r2_score(y_train, train_predictions))
# print("Test R2  :", r2_score(y_test, test_predictions))