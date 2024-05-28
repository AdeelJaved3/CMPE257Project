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
   cd CMPE257Project
   npm install
   ```
4. Launch the frontend
   ```sh
   cd frontend
   npm start
   ```
5. Launch the backend
   ```
   cd backend
   pip3 install -r requirements.txt
   python3 -m venv .venv
   source .venv/bin/activate (for MAC)

   OR

   .venv/Scripts/activate (for Windows)  
   ```
