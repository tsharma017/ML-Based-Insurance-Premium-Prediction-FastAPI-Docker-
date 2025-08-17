# ML-Based-Insurance-Premium-Prediction-FastAPI-Docker

A production-style ML inference API for predicting insurance premium categories from user inputs (age, BMI, lifestyle, etc.).
Built with FastAPI, scikit-learn, pandas, and Uvicorn, and dockerized for easy deployment.

**Project Structure**
```
MI_Insurance_Premium_Prediction/
├─ app.py                    # FastAPI app and routes (/ , /health , /predict)
├─ Dockerfile                # Container build recipe
├─ requirements.txt          # Python dependencies (pinned)
├─ model/
│  ├─ model.pkl              # Trained scikit-learn pipeline
│  └─ predict.py             # Loads model + predict_output() helper
└─ schema/
   ├─ __init__.py
   ├─ user_input.py          # Pydantic v2 schema (UserInput) + computed fields
   └─ config/
      ├─ __init__.py
      └─ city_tier.py        # tier_1_cities, tier_2_cities lists


```

**What This API Does**

- Validates incoming JSON via Pydantic (UserInput).

- Computes features like BMI, age_group, life_style, city_tier.

- Passes a pandas DataFrame into a saved scikit-learn pipeline (model.pkl).

- Returns JSON:

  - predicted_category (string)

  - confidence (float)

  - class_probabilities (dict of label → probability)
 

**Prerequisites**

- Python 3.11+ (3.12 is fine)

- pip (or uv)

- (Optional) Docker if you’ll build/run the container

**1) Run Locally (no Docker)**
1.1 Clone the repository
```
git clone https://github.com/tsharma017/MI_Insurance_Premium_Prediction.git
cd MI_Insurance_Premium_Prediction
```
**1.2 Create & activate a virtual environment**

*macOS / Linux*
```
python3 -m venv myenv
source myenv/bin/activate

```
*Windows (PowerShell)*
```
python -m venv myenv
myenv\Scripts\activate

```
**1.3 Install dependencies**
```
pip install --no-cache-dir -r requirements.txt
```
**1.4 Start the API**
```
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```
- Open Interactive Docs: http://127.0.0.1:8000/docs

- Health check: http://127.0.0.1:8000/health
**1.5 Test the */predict* endpoint**

*Example request*

```
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "weight": 65.0,
    "height": 1.70,
    "income_lpa": 10.0,
    "smoker": true,
    "city": "Mumbai",
    "occupation": "retired"
  }'
```
*Example response*
```
{
  "predicted_category": "medium",
  "confidence": 0.78,
  "class_probabilities": {
    "low": 0.12,
    "medium": 0.78,
    "high": 0.10
  }
}
```

**2) Run with Docker**
*2.1 Build the image*

```
docker build -t tshar017/ml-insurance-premium-api .
```
**2.2 Run the container (localhost)**
```
docker run --rm -p 8000:8000 tshar017/ml-insurance-premium-api

```
Visit http://127.0.0.1:8000/docs to try the API.

***2.3 Tag & push to Docker Hub (optional)***
```
# login first (verify your Docker Hub email if prompted)
docker login

# tag (example: latest)
docker tag tshar017/ml-insurance-premium-api:latest \
  tshar017/ml-insurance-premium-api:latest

# push
docker push tshar017/ml-insurance-premium-api:latest
```

**3) API Contract (Request / Response)**
*3.1 Request JSON (/predict)*

```
{
  "age": 30,
  "weight": 65.0,
  "height": 1.70,
  "income_lpa": 10.0,
  "smoker": true,
  "city": "Mumbai",
  "occupation": "retired"
}
```
- age: int (1–119)

- weight: float (>0, kg)

- height: float (>0, ≤2.5, meters)

- income_lpa: float (>0)

- smoker: bool

- city: string (Title-cased by validator)

- occupation: one of
retired, freelancer, student, government_job, business_owner, unemployed, private_job

**3.2 Derived features (computed server-side)**

- BMI = weight / height²

- life_style = low / medium / heigh

- Note: The project keeps heigh intentionally if the model was trained with that label.

- age_group = young / adult / middle_aged / senior

- city_tier = 1 / 2 / 3 (based on city lists)

**3.3 Response JSON**
```
{
  "predicted_category": "<label>",
  "confidence": <float>,
  "class_probabilities": {
    "<label_1>": <prob>,
    "<label_2>": <prob>,
    "...": "..."
  }
}

```

**4) How the Code Fits Together**

schema/user_input.py
Pydantic v2 model UserInput validates inputs and computes fields (BMI, life_style, age_group, city_tier).
Ensure package imports are relative inside the schema package:
```
from .config.city_tier import tier_1_cities, tier_2_cities
```
Also make sure schema/__init__.py and schema/config/__init__.py exist (even empty).

model/predict.py
Loads model.pkl with a relative Path and exposes:
```
def predict_output(user_input_or_df) -> dict
```
returning predicted_category, confidence, and class_probabilities.
(If your encoder was trained with handle_unknown='ignore', unseen categories won’t crash.)

- app.py
Creates FastAPI app, exposes:

GET / → welcome message

GET /health → status and model version

POST /predict → validates UserInput, builds a one-row DataFrame, calls predict_output(), and returns the prediction dict.

- requirements.txt
Pinned versions of FastAPI, scikit-learn, pandas, numpy, uvicorn, etc., so reproducibility is strong. 

- Dockerfile
Multi-step: copy requirements.txt, install, then copy project code and start Uvicorn.

**5) Example Dockerfile (for reference)**

If your repo already has a Dockerfile, keep using it. This is a minimal, good template:

```
# Use a small Python base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (cache-friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```
**6) Repro Checklist (Fast Path)**

1. Clone → git clone … && cd …

2. Create venv → python -m venv myenv && source myenv/bin/activate

3. Install deps → pip install -r requirements.txt

4. Run API → uvicorn app:app --reload

5. Open docs → http://127.0.0.1:8000/docs

6. Test predict → POST sample JSON

7. Docker build → docker build -t <you>/ml-insurance-premium-api .

8. Docker run → docker run -p 8000:8000 <you>/ml-insurance-premium-api

9. (Optional) Push → docker login && docker push <you>/ml-insurance-premium-api:latest


**7) Troubleshooting**

- ImportError: cannot import name 'UserInput'

  Ensure schema/__init__.py and schema/config/__init__.py exist.

  Use relative import in schema/user_input.py:
```
from .config.city_tier import tier_1_cities, tier_2_cities
```

 Start Uvicorn from the project root (where schema/ exists).

- ValueError: Found unknown categories ['high'] …
Your model’s OneHotEncoder never saw 'high' during training (e.g., you trained with 'heigh').

  Short-term: keep returning 'heigh' in life_style to match training.

  Long-term: retrain with OneHotEncoder(handle_unknown='ignore') and correct label spelling.

- AttributeError: Can't get attribute '_RemainderColsList' on unpickle
  Mismatch between scikit-learn version used for training vs inference.

  Align versions (use the pinned ones in requirements.txt).

  Re-export model with the current version if needed.

- Docker 401 / cannot pull python:3.12-slim

  Verify Docker Hub email → docker login → retry docker pull python:3.12-slim.

  Remove corrupted creds: mv ~/.docker/config.json ~/.docker/config.json.bak → docker login.

**8) License & Acknowledgements**

Built by Tejendra Sharma (tsharma017)

Uses open-source libraries listed in requirements.txt. 
