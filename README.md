# Cyberbullying Detection System
## This project uses the support vector machine, XGBoost and RoBERTa machine learning architectures to detect tweets that contain different forms of cyberbullying.

The purpose of this project is to preprocess data and then use the processed data to train several machine learning models. The data contains over 47,000 tweets, in tabular form, provided from Kaggle and a scholarly article. One of the main objectives is to reproduce and outperform models on the same dataset found in this scholarly article <a href="https://arxiv.org/pdf/2402.04088">The Use of a Large Language Model for Cyberbullying Detection</a>. 
The best performing model is used in a small web application to demonstrate the effectiveness in classifying cyberbullying text.

## How to download and use the trained RoBERTa model via web application

Here are the steps for launching the web application.

1. Navigate to preferred directory
    ```sh
   cd <directory>
   ```
2. Clone the repository
   ```sh
   git clone https://github.com/AdeelJaved3/CMPE257Project.git
   ```
3. Install NPM packages
   ```sh
   cd CMPE257Project/frontend
   npm install
   ```
4. Launch the frontend
   ```sh
   npm start
   ```
5. Activating the virtual environment
   ```
   cd ..
   cd backend
   python3 -m venv .venv
   
   source .venv/bin/activate (for MAC)
   OR
   .venv/Scripts/activate (for Windows)

   pip3 install -r requirements.txt
   ```
6. Launching the backend
   ```
   export FLASK_APP=server.py
   export FLASK_ENV=development
   flask run
   ```
   

## How to tweak this project for your own uses

1. Adopt the preprocessing logic to clean text, remove stop words and balance multiple classes
2. Adopt the CountVectorizer and/or TF-IDF feature extraction techniques used with SVM
3. Adopt RoBERTa, SVM, or XGBoost implementation for your own cyberbullying dataset

## Find a bug?

If you have found an issue and would like to improve the project, please submit an issue using the issue tab above. If you would like to sumbit a PR with a fix, reference the issue you created.


