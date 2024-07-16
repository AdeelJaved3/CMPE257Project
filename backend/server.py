from flask import Flask, request, jsonify
import torch
from transformers import AutoTokenizer, pipeline

app = Flask(__name__)


def load_model_and_tokenizer():
    try:
        saved_model = torch.load("./RobertaModel/RobertaModel.pt", map_location=torch.device('cpu'))
        tokenizer = AutoTokenizer.from_pretrained('roberta-base')
        classifier = pipeline("text-classification", model=saved_model, tokenizer=tokenizer)
        return classifier
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise RuntimeError("Error loading model") from e  # Chain the exception


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

    except Exception as e:
        print(e)
        return jsonify({'error': 'Unexpected error occurred'}), 500


if __name__ == "__main__":
    app.run(debug=True)
