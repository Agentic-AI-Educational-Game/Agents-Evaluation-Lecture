from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from utils.transcription import transcribe_audio
from utils.accuracy import calculate_accuracy
from utils.speed import calculate_wpm
from utils.fluency import detect_fluency
from utils.pronunciation import get_pronunciation_feedback
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from bson import ObjectId
import json

app = Flask(__name__)
CORS(app)

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'speech_evaluation')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'evaluations')

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def serialize_response(data):
    """Convert ObjectId to string for JSON serialization"""
    if isinstance(data, dict):
        return {k: serialize_response(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [serialize_response(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data


@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        # Validate input
        if 'audio' not in request.files or 'expected_text' not in request.form:
            return jsonify({"error": "Missing audio or expected_text"}), 400

        audio_file = request.files['audio']
        expected_text = request.form['expected_text']

        # Save audio file
        filename = secure_filename(audio_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(file_path)

        # Process audio and calculate metrics
        transcript, segments = transcribe_audio(file_path)
        accuracy = calculate_accuracy(transcript, expected_text)
        total_duration = segments[-1]['end'] - segments[0]['start']
        wpm = calculate_wpm(len(transcript.split()), total_duration)
        fluency = detect_fluency(segments)
        pron_feedback = get_pronunciation_feedback(transcript, expected_text)

        # Calculate score
        score_val = (accuracy / 100 + wpm / 100 + (
            1 if fluency == 'excellent' else 0.8 if fluency == 'good' else 0.5)) / 3
        score = round(score_val * 5, 1)

        # Prepare response data
        response_data = {
            "accuracy": f"{accuracy}%",
            "speed": f"{wpm} WPM",
            "fluency": fluency,
            "pron_feedback": pron_feedback,
            "score": score,
            "transcript": transcript
        }

        # Prepare document for MongoDB
        document = {
            "timestamp": datetime.utcnow(),
            "expected_text": expected_text,
            "transcript": transcript,
            "accuracy": accuracy,
            "speed_wpm": wpm,
            "fluency": fluency,
            "pronunciation_feedback": pron_feedback,
            "score_value": score_val,
            "score_display": score,
            "audio_filename": filename,
            "duration": total_duration,
            "segments": segments,
            "response_data": response_data
        }

        # Store in MongoDB
        result = collection.insert_one(document)

        # Add the MongoDB document ID to response (optional)
        # response_data["evaluation_id"] = str(result.inserted_id)

        # Clean up audio file (optional)
        try:
            os.remove(file_path)
        except OSError:
            pass  # File removal failed, but continue

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/evaluations', methods=['GET'])
def get_evaluations():
    """Retrieve all evaluations from MongoDB"""
    try:
        evaluations = list(collection.find().sort("timestamp", -1))
        return jsonify(serialize_response(evaluations))
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve evaluations: {str(e)}"}), 500


@app.route('/evaluations/<evaluation_id>', methods=['GET'])
def get_evaluation(evaluation_id):
    """Retrieve a specific evaluation by ID"""
    try:
        evaluation = collection.find_one({"_id": ObjectId(evaluation_id)})
        if evaluation:
            return jsonify(serialize_response(evaluation))
        else:
            return jsonify({"error": "Evaluation not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve evaluation: {str(e)}"}), 500


@app.route('/evaluations/<evaluation_id>', methods=['DELETE'])
def delete_evaluation(evaluation_id):
    """Delete a specific evaluation by ID"""
    try:
        result = collection.delete_one({"_id": ObjectId(evaluation_id)})
        if result.deleted_count:
            return jsonify({"message": "Evaluation deleted successfully"})
        else:
            return jsonify({"error": "Evaluation not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to delete evaluation: {str(e)}"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test MongoDB connection
        client.admin.command('ping')
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)