import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_predict(self):
        response = client.post("/predict", json={
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
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("prediction", response.json())
