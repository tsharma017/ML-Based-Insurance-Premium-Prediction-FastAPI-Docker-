from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pickle
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION
import pandas as pd

# create app object
app = FastAPI()


# to give clear message about the URL
@app.get('/')
def home():
    return {'message': 'ML based Insurance Premium Prediction API'}


# API is live and healthy and which is machine readale for AWS
@app.get('/health')
def health_check():
    return {
        'status': 'OK',

        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }


@app.post('/predict', resposnse_model = PredictionResponse)
def predict_premium(data: UserInput):

    user_input = pd.DataFrame([{
        'BMI': data.BMI,
        'age_group': data.age_group,
        'life_style': data.life_style,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

# always good to have try catch 
    try:

        prediction = predict_output(user_input)

        return JSONResponse(status_code = 200, content = {'predicted_category': prediction})

    except Exception as e:

        return JSONResponse(status_code = 500, content = str(e))

