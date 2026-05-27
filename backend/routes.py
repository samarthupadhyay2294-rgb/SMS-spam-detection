import os
from flask import Blueprint, jsonify, request, current_app
from backend.utils.predictor import predict_message
from backend.database.db import save_prediction, get_history

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint to verify server status."""
    return jsonify({"status": "ok"}), 200

@api_bp.route('/predict', methods=['POST'])
def predict():
    """
    Spam detection prediction endpoint.
    Expects JSON body: { "message": "text to analyze" }
    """
    data = request.get_json(silent=True)
    
    # 1. Validation
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid request body. Expected JSON data."}), 400
        
    message = data.get('message')
    
    if message is None:
        return jsonify({"error": "Missing 'message' field in request body."}), 400
        
    if not isinstance(message, str):
        return jsonify({"error": "The 'message' field must be a string."}), 400
        
    if not message.strip():
        return jsonify({"error": "The 'message' field cannot be empty or whitespace."}), 400
        
    if len(message) > 1000:
        return jsonify({"error": "The message exceeds the maximum length of 1000 characters."}), 400
        
    try:
        # Run prediction pipeline
        result = predict_message(message)
        
        # Save to backend database for persistent log tracking
        db_path = current_app.config['DB_PATH']
        save_prediction(
            db_path=db_path,
            message=message,
            prediction=result['prediction'],
            confidence=result['confidence'],
            risk_level=result['risk_level'],
            probability=result['probability'],
            keywords=result['keywords']
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        current_app.logger.error(f"Prediction Error: {str(e)}")
        return jsonify({"error": f"Internal prediction engine failure: {str(e)}"}), 500

@api_bp.route('/api/history', methods=['GET'])
def api_history():
    """
    Exposes SQLite prediction logs history database.
    Returns the latest 10 prediction results.
    """
    try:
        db_path = current_app.config['DB_PATH']
        history = get_history(db_path, limit=10)
        return jsonify(history), 200
    except Exception as e:
        current_app.logger.error(f"History Fetch Error: {str(e)}")
        return jsonify({"error": f"Failed to retrieve scan history: {str(e)}"}), 500
