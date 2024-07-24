from flask import Flask, request, jsonify
import boto3
import onnxruntime as ort
from transformers import AutoTokenizer
from dotenv import load_dotenv
import numpy as np
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# AWS S3 configuration
AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
MODEL_KEY = os.getenv('MODEL_KEY')  # Replace with your model file key in S3

def load_model_and_tokenizer():
    try:
        model_path = "RobertaModel.onnx"
        
        # Check if local file exists
        if os.path.exists(model_path):
            logger.info("Model found locally")
        else:
            # Initialize S3 client
            s3 = boto3.client('s3', region_name=AWS_REGION,
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            logger.info("Connected to S3, downloading model....")

            # Download model from S3
            with open(model_path, "wb") as f:
                s3.download_fileobj(AWS_BUCKET_NAME, MODEL_KEY, f)
                
            # Verify the file size to check if download was successful
            file_size = os.path.getsize(model_path)
            if file_size == 0:
                raise RuntimeError("Downloaded model file is empty")

        # Load the tokenizer
        tokenizer = AutoTokenizer.from_pretrained('roberta-base')

        # Load the ONNX model
        session = ort.InferenceSession(model_path)

        logger.info("Model loaded successfully")
        return session, tokenizer

    except boto3.exceptions.S3UploadFailedError as e:
        logger.error(f"Error downloading model from S3: {str(e)}")
        raise RuntimeError("Error downloading model from S3") from e
    except Exception as e:
        logger.error(f"General error: {str(e)}")
        raise RuntimeError("An unexpected error occurred while loading the model") from e

session = None
tokenizer = None

@app.route('/')
def index():
    return "Cyberbullying Detection System Server running"

@app.route('/test-model', methods=['POST'])
def test_model():
    global session, tokenizer

    try:
        if request.method == 'POST':
            data = request.get_json()
            text = data.get('text', '')

            if not text:
                raise ValueError('Empty or missing text field in request')

            if session is None or tokenizer is None:
                session, tokenizer = load_model_and_tokenizer()  # Load on first request

            # Tokenize the input text
            inputs = tokenizer(text, return_tensors="np", padding='max_length', truncation=True, max_length=6)
            ort_inputs = {session.get_inputs()[0].name: inputs["input_ids"].astype(np.int64)}

            ort_outputs = session.run(None, ort_inputs)
            
            OP_label = {
                'LABEL_0': 'Non Cyberbullying',
                'LABEL_1': 'Age',
                'LABEL_2': 'Ethnicity',
                'LABEL_3': 'Religion',
                'LABEL_4': 'Gender',
                'LABEL_5': 'Other Cyberbullying'
            }

            label_id = ort_outputs[0].argmax()
            label = OP_label[f'LABEL_{label_id}']
            response_data = {'result': label}

            return jsonify(response_data)

    except ValueError as ve:
        logger.warning(ve)
        return jsonify({'error': str(ve)}), 400

    except RuntimeError as re:
        logger.error(re)
        return jsonify({'error': str(re)}), 500

    except Exception as e:
        logger.error(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == "__main__":
    app.run(debug=True)
