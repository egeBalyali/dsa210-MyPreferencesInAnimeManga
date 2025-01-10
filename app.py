import pickle
from flask import Flask, request, render_template
import re

app = Flask(__name__)

# Load the pre-trained regression model
with open('anime_score_predictor.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    
    # Extract the ID from the URL (adjust this regex to match your URL structure)
    
    if match:
        url_id = int(match.group(1))
    else:
        return "Invalid URL", 400
    
    # Use the model to predict a score based on the URL ID (or extracted features)
    prediction = model.predict([[url_id]])  # Adjust this part depending on model input
    return f"Predicted Score: {prediction[0]}"

if __name__ == '__main__':
    app.run(debug=True)
