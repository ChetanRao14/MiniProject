from flask import Flask, request, jsonify
import joblib
import pandas as pd
import warnings

# Suppress specific warnings from scikit-learn about version mismatch
# This is common and usually not a problem.
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

# --- 1. Create the Flask App ---
app = Flask(__name__)

# --- 2. Load The Trained Models ---
# We load these once when the server starts to be fast.
try:
    model_category = joblib.load('model_category.joblib')
    model_priority = joblib.load('model_priority.joblib')
    print("Models loaded successfully.")
except FileNotFoundError:
    print("Error: Model files not found. Run 'train.py' first.")
    exit()
except Exception as e:
    print(f"Error loading models: {e}")
    exit()

# --- 3. Define the API Endpoint ---
# This creates a URL at '/predict' that accepts POST requests
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the JSON data from the request
        # We expect data in the format: { "text": "some complaint text" }
        json_data = request.get_json()
        
        if not json_data or 'text' not in json_data:
            return jsonify({'error': "Missing 'text' key in JSON payload"}), 400

        # Get the complaint text from the JSON
        complaint_text = json_data['text']
        
        # We must put the text into a list or pandas Series
        # because the model was trained on a series of texts.
        text_to_predict = pd.Series([complaint_text])

        # --- Make Predictions ---
        category_prediction = model_category.predict(text_to_predict)
        priority_prediction = model_priority.predict(text_to_predict)

        # --- Format the Response ---
        # .tolist()[0] gets the first item from the prediction array (e.g., 'Water')
        response = {
            'category': category_prediction.tolist()[0],
            'priority': priority_prediction.tolist()[0]
        }
        
        # Send the response back as JSON
        return jsonify(response)
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500

# --- 4. Run the App ---
if __name__ == '__main__':
    # This makes the server accessible on your network
    # (e.g., from your Node.js backend)
    print("Starting Flask API server at http://0.0.0.0:5000/ ...")
    app.run(host='0.0.0.0', port=5000, debug=True)