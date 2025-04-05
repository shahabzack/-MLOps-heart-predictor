from fastapi import FastAPI
from pydantic import BaseModel, Field
from enum import Enum
import numpy as np
import pandas as pd
import xgboost as xgb
import warnings

warnings.filterwarnings("ignore")

# 🔥 Load XGBoost Booster model
model = xgb.Booster()
model.load_model("models/model1.json")  # Ensure this path is correct

app = FastAPI(title="Heart Disease Prediction API")


# Enums
class SexEnum(int, Enum):
    male = 1
    female = 0

class ChestPainEnum(int, Enum):
    typical_angina = 0
    atypical_angina = 1
    non_anginal_pain = 2
    asymptomatic = 3

class FbsEnum(int, Enum):
    yes = 1
    no = 0

class RestECGEnum(int, Enum):
    normal = 0
    st_abnormality = 1
    lv_hypertrophy = 2

class ExAngEnum(int, Enum):
    yes = 1
    no = 0

class SlopeEnum(int, Enum):
    upsloping = 0
    flat = 1
    downsloping = 2

class ThalEnum(int, Enum):
    normal = 1
    fixed_defect = 2
    reversible_defect = 3

# Input schema
class HeartInput(BaseModel):
    age: int
    sex: SexEnum
    cp: ChestPainEnum
    trestbps: int
    chol: int
    fbs: FbsEnum
    restecg: RestECGEnum
    thalach: int
    exang: ExAngEnum
    oldpeak: float
    slope: SlopeEnum
    ca: int = Field(..., ge=0, le=3)
    thal: ThalEnum

    class Config:
        schema_extra = {
            "example": {
                "age": 60,
                "sex": 1,
                "cp": 2,
                "trestbps": 140,
                "chol": 240,
                "fbs": 0,
                "restecg": 1,
                "thalach": 160,
                "exang": 0,
                "oldpeak": 1.4,
                "slope": 2,
                "ca": 0,
                "thal": 2
            }
        }

# Prediction endpoint
@app.post("/predict")
def predict(data: HeartInput):
    features = [
        data.age,
        data.sex.value,
        data.cp.value,
        data.trestbps,
        data.chol,
        data.fbs.value,
        data.restecg.value,
        data.thalach,
        data.exang.value,
        data.oldpeak,
        data.slope.value,
        data.ca,
        data.thal.value
    ]

    feature_names = [
        "age", "sex", "cp", "trestbps", "chol",
        "fbs", "restecg", "thalach", "exang",
        "oldpeak", "slope", "ca", "thal"
    ]

    input_df = pd.DataFrame([features], columns=feature_names)
    dmatrix = xgb.DMatrix(input_df)
    y_prob = model.predict(dmatrix)

    result = "Heart Disease" if y_prob[0] > 0.5 else "No Heart Disease"
    return {
        "prediction": result,
        "confidence": round(float(y_prob[0]) * 100, 2)
    }
