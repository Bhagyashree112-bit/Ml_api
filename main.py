from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Load your trained model
with open("heart_disease_model.pkl", "rb") as f:
    model = pickle.load(f)

# Create FastAPI app
app = FastAPI()

# Define input format
class UserInput(BaseModel):
    age: int
    sex: int
    bp: int
    cholesterol: int

# Home route
@app.get("/")
def home():
    return {"message": "Model API is running"}

# Prediction route
@app.post("/predict")
def predict(data: UserInput):
    # Convert input to array
    input_data = np.array([[data.age, data.sex, data.bp, data.cholesterol]])
    
    # Make prediction
    prediction = model.predict(input_data)
    
    # Return result
    return {"prediction": int(prediction[0])}