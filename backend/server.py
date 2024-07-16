from flask import Flask, request, jsonify
import boto3
import torch
from transformers import AutoTokenizer, pipeline
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)

# AWS S3 configuration
AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
MODEL_KEY = os.getenv('MODEL_KEY')  # Replace with your model file key in S3

def load_model_and_tokenizer():
    try:
        # Check if local file exists
        if os.path.exists("./models/RobertaModel.pt"):
            model_path = "./models/RobertaModel.pt"
        else:
            # Initialize S3 client
            s3 = boto3.client('s3', region_name=AWS_REGION,
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

            # Download model from S3
            with open("RobertaModel.pt", "wb") as f:
                s3.download_fileobj(AWS_BUCKET_NAME, MODEL_KEY, f)
            
            model_path = "RobertaModel.pt"

        # Load the model and tokenizer
        saved_model = torch.load(model_path, map_location=torch.device('cpu'))
        tokenizer = AutoTokenizer.from_pretrained('roberta-base')
        classifier = pipeline("text-classification", model=saved_model, tokenizer=tokenizer)
        print("Model loaded successfully")
        return classifier

    except boto3.exceptions.S3UploadFailedError as e:
        print(f"Error downloading model from S3: {str(e)}")
        raise RuntimeError("Error downloading model from S3") from e
    except Exception as e:
        print(f"General error: {str(e)}")
        raise RuntimeError("An unexpected error occurred while loading the model") from e

classifier = None

@app.route('/')
def index():
    return "Cyberbullying Detection System Server running"

@app.route('/test-model', methods=['POST'])
def test_model():
    global classifier

    try:
        if request.method == 'POST':
            data = request.get_json()
            text = data.get('text', '')

            if not text:
                raise ValueError('Empty or missing text field in request')

            if classifier is None:
                classifier = load_model_and_tokenizer()  # Load on first request

            OP_label = {
                'LABEL_0': 'Non Cyberbullying',
                'LABEL_1': 'Age',
                'LABEL_2': 'Ethnicity',
                'LABEL_3': 'Religion',
                'LABEL_4': 'Gender',
                'LABEL_5': 'Other Cyberbullying'
            }

            res = classifier(text)
            label = OP_label[res[0]["label"]]
            response_data = {'result': label}

            return jsonify(response_data)

    except ValueError as ve:
        print(ve)
        return jsonify({'error': str(ve)}), 400

    except RuntimeError as re:
        print(re)
        return jsonify({'error': str(re)}), 500

    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500


if __name__ == "__main__":
    app.run(debug=True)
