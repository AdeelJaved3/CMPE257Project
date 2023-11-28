import streamlit as st
import joblib  # Use joblib or your preferred library to load your pre-trained model

# Load your pre-trained XGBoost model here
model = joblib.load('cyber_bullying_XGB.pkl')  # Replace 'your_pretrained_model.pkl' with your model file path

# Define the Streamlit app
st.title("Cyberbullying Detection App")

# Add a text input widget for user input
user_input = st.text_input("Enter text:")

# Create a button to trigger the prediction
if st.button("Predict"):
    # Preprocess the user input (similar to your training data preprocessing)
    # Pass the preprocessed input through your XGBoost model for prediction
    # Make sure to convert the input text into the format expected by your model (e.g., TF-IDF vectors)

    # Perform the prediction
    prediction = model.predict([user_input])  # Replace with the actual prediction code

    # Display the prediction result to the user
    if prediction[0] == 3:
        st.write("Cyberbullying Detected")
    else:
        st.write("No Cyberbullying Detected")
