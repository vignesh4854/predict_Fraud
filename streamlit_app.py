try:
    import streamlit as st
    import joblib
    import numpy as np
except ModuleNotFoundError as e:
    print("Error: Required module not found. Ensure you have 'streamlit' installed in your environment.")
    raise e

# Load the trained model
try:
    loaded_model = joblib.load("best_model.joblib")
except FileNotFoundError as e:
    print("Error: Model file not found. Ensure 'best_model.joblib' exists in the correct directory.")
    loaded_model = None

# Define encoding mappings
age_mapping = {"<= 18": 0, "19-25": 1, "26-35": 2, "36-45": 3, "46-55": 4, "56-65": 5, "> 65": 6, "Unknown": 7}
gender_mapping = {"Male": 2, "Female": 1, "Enterprise": 0, "Unknown": 3}
category_mapping = {"Food": 3, "Transportation": 12, "Health": 4, "Others": 9, "Hotel Services": 6,
                    "Bars and Restaurants": 0, "Tech": 11, "Sports and Toys": 10, "Wellness and Beauty": 14,
                    "Hyper": 7, "Fashion": 2, "Home": 5, "Contents": 1, "Travel": 13, "Leisure": 8}

# Streamlit UI
st.title("Fraud Detection System")

# Input fields
transaction_id = st.text_input("Transaction ID", "5567893")
merchant_id = st.text_input("Merchant ID", "3452234")
age_category = st.selectbox("Age Category", list(age_mapping.keys()))
gender = st.selectbox("Gender", list(gender_mapping.keys()))
category = st.selectbox("Category", list(category_mapping.keys()))
amount = st.number_input("Amount", min_value=1, value=1640)

# Predict button
if st.button("Predict"):
    if loaded_model is None:
        st.error("Model file not found. Please ensure 'best_model.joblib' is in the correct directory.")
    else:
        try:
            # Convert inputs to encoded values
            input_data = np.array([[int(transaction_id), int(merchant_id), age_mapping[age_category],
                                     gender_mapping[gender], category_mapping[category], amount]])
            
            # Make prediction
            prediction = loaded_model.predict(input_data)
            result = "Fraudulent" if prediction[0] == 1 else "Not Fraudulent"
            
            # Display result
            st.write(f"### The prediction is: {result}")
        except ValueError as e:
            st.error("Invalid input values. Please check your inputs and try again.")
            raise e
