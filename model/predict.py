import pickle
import pandas as pd 
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "model.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# step 1: import ML model
#with open('/Users/tejsharma/Desktop/MI_Insurance_Premium_Prediction/model/model.pkl', 'rb') as f:
#    model = pickle.load(f)

# MLFLOW will automatically track your model versio but this one is just the manual 

MODEL_VERSION = '1.0.0'

# get the class labels from model (important for matching probalilities to class names)

class_labels = model.classes_.tolist()



def predict_output(user_input: dict):

    df = pd.DataFrame([user_input])

    # predict the class
    predicted_class = model.predict(df)[0]

    # Get probabilities for all classes 
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)

    # Createmapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }

   