import pandas as pd
import matplotlib.pyplot as plt
from neuralprophet import NeuralProphet

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 1000)

MINUTES = 15  # time interval on which the data should be sampled down
DAYS_FUTURE = 3  # how many days should be predicted
DAYS_PAST = 1  # how many past days should be plotted
LAG_HOURS = 100  # how many hours should be used to predict the future

horizon = (DAYS_FUTURE * 24 * 60) // MINUTES
past = (DAYS_PAST * 24 * 60) // MINUTES

# (1) Load the data
data = pd.read_csv('../crawler/data.csv', header=None, names=['timestamp', 'y'])
data['ds'] = pd.to_datetime(data['timestamp'], unit='s').dt.tz_localize('UTC')
data['ds'] = data['ds'].dt.tz_convert('Europe/Berlin').dt.tz_localize(None)
data = data.drop("timestamp", axis=1)
data['y'] = data['y'] / 100
# Resample the data and fill missing values with interpolation
data = data.set_index("ds").resample(f"{MINUTES}T").mean().interpolate().reset_index()

# (2) Train the model
prophet = NeuralProphet(
    daily_seasonality=True,
    weekly_seasonality=True,
    learning_rate=0.001,
    batch_size=64,
    n_forecasts=horizon,
    n_lags=LAG_HOURS * MINUTES,
)
metrics = prophet.fit(data, progress='plot', freq=f"{MINUTES}T")

# (3) Predict the next day
future = prophet.make_future_dataframe(data, periods=horizon, n_historic_predictions=len(data))
forecast = prophet.predict(future)

# (4) Visualize the results
fig, ax = plt.subplots(figsize=(10, 6))
# Plot the actual data
ax.plot(data['ds'].tail(past), data['y'].tail(past), label='Actual', linewidth=1)

# Plot the future predictions
future_ds = forecast['ds'].tail(horizon)
future_yhats = forecast[f'yhat{horizon}'].tail(horizon).clip(lower=0.05)
ax.plot(future_ds, future_yhats, label='Future Predictions', linewidth=1, linestyle="--")

ax.legend()
ax.set_xlabel("Date")
ax.set_ylabel("Rate")
ax.grid(True)

# save the image
fig.save("prediction.png")
