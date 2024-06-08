import json
import numpy as np
import pandas as pd
from azureml.core.model import Model
import joblib

def init():
    global model
    model_path = Model.get_model_path('chembl_model')
    model = joblib.load(model_path)

def run(data):
    try:
        data = json.loads(data)
        input_data = pd.DataFrame.from_dict(data['data'])
        predictions = model.predict(input_data)
        return json.dumps({"predictions": predictions.tolist()})
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})
