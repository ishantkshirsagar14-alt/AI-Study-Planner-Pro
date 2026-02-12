import numpy as np
from sklearn.linear_model import LinearRegression

def train_model():
    np.random.seed(42)

    hours = np.random.randint(1, 10, 100)
    days = np.random.randint(1, 30, 100)
    difficulty = np.random.randint(1, 4, 100)

    performance = (hours * 5) + (days * 1.5) - (difficulty * 3)

    X = np.column_stack((hours, days, difficulty))
    y = performance

    model = LinearRegression()
    model.fit(X, y)

    return model
