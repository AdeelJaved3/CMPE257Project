from flask import Flask, request, jsonify
import torch
from transformers import AutoTokenizer, pipeline

app = Flask(__name__)

@app.route('/test-model', methods=['GET','POST'])
def test_model():

    if request.method == 'POST':
        data = request.get_json()

    print(data)
    classifier = prepare_model()

    OP_label = {'LABEL_0': 'Non Cyberbullying', 'LABEL_1': 'Age',
                'LABEL_2': 'Ethnicity', 'LABEL_3': 'Religion',
                'LABEL_4': 'Gender', 'LABEL_5': 'Other Cyberbullying'}

    res = classifier(data['text'])
    label = OP_label[res[0]["label"]]

    response_data = {'result': label}
    return jsonify(response_data)

def prepare_model():
    saved_model = torch.load("/Users/admin/Desktop/CMPE_257/Cyber_Bullying_Detection_System/CMPE257Project/saved_RoBERTa_model/RobertaModel.pt")
    tokenizer_identifier = "roberta-base"
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_identifier)
    classifier = pipeline("text-classification", model=saved_model,tokenizer=tokenizer)
    return classifier

if __name__ == "__main__":
    app.run(debug=True)
