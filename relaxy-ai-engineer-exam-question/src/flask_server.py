from flask import Flask, request,Response,jsonify
import mlflow
import mlflow.pyfunc
import sqlite3
import json
from datetime import datetime
import pandas as pd
import time
app = Flask(__name__)

# Load the model once at startup
try:
    model = mlflow.pyfunc.load_model("/root/code/Loan-Approval-Model/relaxy-ai-engineer-exam-question/mlruns/0/1612dcd8f8d049a78790ebf67e9a27ee/artifacts/model")
    model_loaded = True
except Exception as e:
    model_loaded = False
    model_error = str(e)

@app.route('/health', methods=['GET'])
def health_check():
    # Check API status
    api_status = "ok"
    model_status = model_loaded
    db_status = "ok"
    try:
        conn = sqlite3.connect("mlruns.db")
        conn.execute("SELECT 1")
        conn.close()
    except Exception as e:
        db_status = f"Database connection failed: {str(e)}"
    
   
    dependencies_ok = True
    
    # Manually create JSON with explicit key order
    response_data = {
        "status": "healthy" if model_status and db_status == "ok" else "unhealthy",
        "checks": {
            "model_loaded": model_status,
            "api_status": api_status,
            "model_version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
        }
    }
    
    return Response(json.dumps(response_data), mimetype='application/json')

def feature_engineering(X: pd.DataFrame) -> pd.DataFrame:
    """Perform feature engineering on the dataset"""
    X = X.copy()
    
    # Calculate derived features
    X['loan_to_income_ratio'] = X['loan_amount'] / X['income_annum']
    X['total_asset_value'] = (X['residential_assets_value'] +
                               X['commercial_assets_value'] +
                               X['luxury_assets_value'] +
                               X['bank_asset_value'])
    X['income_per_dependent'] = X['income_annum'] / (X['no_of_dependents'] + 1)
    
    # Create CIBIL category columns
    if 'cibil_score' in X.columns:
        X['cibil_category_Low'] = (X['cibil_score'] < 500).astype(int)
        X['cibil_category_Medium'] = ((X['cibil_score'] >= 500) & (X['cibil_score'] <= 700)).astype(int)
    
    return X

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        # Convert data to DataFrame
        input_data = pd.DataFrame([data])  # Adjust if multiple records are supported
        
        X_transformed = feature_engineering(input_data)

        # Categorical features to encode
        categorical_features = ['education', 'self_employed']

        # Perform one-hot encoding while keeping all original features
        X_encoded = pd.get_dummies(
            X_transformed, 
            columns=categorical_features, 
            prefix=categorical_features,  # Use feature names as prefix
            drop_first=False  # Keep all categories
        )
        
        prediction = model.predict(X_encoded).tolist()

        
        # Create a response
        response = {
            "prediction": prediction[0],  # Ensure the output is JSON serializable
            "model_version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),   
        }
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Return 400 for client errors
@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        instances = data['instances']
        start_time = time.time()
        # List to store predictions
        predictions_list = []
        
        # Loop through each sample and predict
        for i,sample in enumerate(instances):
            # Convert single sample to DataFrame
            print(sample)
            input_data = pd.DataFrame([sample])
            # Feature engineering
            X_transformed = feature_engineering(input_data)
            
            # Categorical features to encode
            categorical_features = ['education', 'self_employed']
            
            # One-hot encoding
            X_encoded = pd.get_dummies(
                X_transformed, 
                columns=categorical_features, 
                prefix=categorical_features,
                drop_first=False
            )
            
            # Predict for single sample
            prediction = model.predict(X_encoded).tolist()
            
            # Add prediction to list (convert to float to ensure JSON serializability)
            predictions_list.append({
                "prediction": prediction[0],
                "row_id": i
            })
        processing_time = time.time() - start_time
        # Create response
        response = {
            "predictions": predictions_list,
            "model_version": "1.0.0",
            "batch_size": len(predictions_list),
            "timestamp": datetime.utcnow().isoformat(),
            "processing_time":processing_time
            
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)