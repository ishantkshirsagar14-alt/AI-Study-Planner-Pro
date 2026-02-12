import numpy as np
import pandas as pd

def generate_study_plan(subjects, weights, total_hours):
    total_weight = sum(weights)
    allocated_hours = [(w / total_weight) * total_hours for w in weights]

    df = pd.DataFrame({
        "Subject": subjects,
        "Difficulty Weight": weights,
        "Daily Allocated Hours": np.round(allocated_hours, 2)
    })

    return df, allocated_hours
