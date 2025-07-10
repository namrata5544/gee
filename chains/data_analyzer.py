import json
from sklearn.linear_model import LinearRegression
import numpy as np

def analyze_data():
    with open("output/gee_output.json") as f:
        data = json.load(f)  # Assumed format: {"dates": [...], "values": [...]}

    X = np.arange(len(data["values"])).reshape(-1, 1)
    y = np.array(data["values"])

    model = LinearRegression()
    model.fit(X, y)

    trend = model.coef_[0]
    return {"trend": trend, "summary": f"Trend is {'increasing' if trend > 0 else 'decreasing'}"}
