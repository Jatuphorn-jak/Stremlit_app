import streamlit as st
import pandas as pd
import numpy as np
#import pickle
import joblib
from sklearn.linear_model import LinearRegression
print(np.__version__)
# Load the trained model
with open("model.pkl", "rb") as f:
    model = joblib.load(f)
    

# Set page configuration
st.set_page_config(page_title="ML Prediction App", layout="wide")

# Sidebar for navigation
page = st.sidebar.radio("Select a Page", ["Home", "Page 1", "Page 2"])


# Home Page: Login with name input
if page == "Home":
    st.title("Home")
    st.write("Please enter your name to continue.")
    name = st.text_input("Enter your name", "")
    
    if name:
        st.write(f"Welcome, {name}! Click 'Page 1' from the sidebar to start using the prediction model.")
        st.session_state.name = name  # Store the name in session_state after the user inputs it.

# Page 1: Simulation input and model prediction
elif page == "Page 1":
    st.title("Page 1 - Predict with Model")
    
    # Check if the name has been entered in session_state
    if 'name' in st.session_state:
        st.write(f"Welcome back, {st.session_state.name}!")
    else:
        st.write("Please go to the Home page and enter your name first.")
    
    # Get inputs for the model prediction
    st.write("### Enter inputs for prediction")
    feature1 = st.number_input("Feature 1", min_value=0.0, max_value=1.0, step=0.01, value=0.5)
    feature2 = st.number_input("Feature 2", min_value=0.0, max_value=1.0, step=0.01, value=0.5)
    
    # Predict button
    if st.button("Predict"):
        # Prepare input data for the model
        input_data = np.array([[feature1, feature2]])
        prediction = model.predict(input_data)
        
        st.write(f"### Prediction Result: {prediction[0]:.2f}")
        st.session_state.prediction = prediction[0]
        st.session_state.feature1 = feature1
        st.session_state.feature2 = feature2

    # Display previous predictions
    if 'prediction' in st.session_state:
        st.write(f"Last prediction: {st.session_state.prediction:.2f}")

# Page 2: Data dashboard displaying previous predictions
elif page == "Page 2":
    st.title("Page 2 - Prediction Dashboard")
    st.write("### Prediction History and Dashboard")
    
    # Check if the prediction data exists in session_state
    if 'feature1' in st.session_state and 'feature2' in st.session_state and 'prediction' in st.session_state:
        # Create a new row of data
        new_data = pd.DataFrame({
            "Feature1": [st.session_state.feature1],
            "Feature2": [st.session_state.feature2],
            "Prediction": [st.session_state.prediction]
        })
        
        # Initialize the predictions dataframe if it's the first time
        if 'predictions_df' not in st.session_state:
            st.session_state.predictions_df = pd.DataFrame(columns=["Feature1", "Feature2", "Prediction"])
        
        # Concatenate the new data with the existing predictions_df
        st.session_state.predictions_df = pd.concat([st.session_state.predictions_df, new_data], ignore_index=True)
        
        # Show prediction history with the new data included
        st.write("### Prediction History (Including New Data)")
        st.dataframe(st.session_state.predictions_df)

        # Display prediction chart for visualizing trends
        if not st.session_state.predictions_df.empty:
            st.write("### Prediction Visualization")
            st.line_chart(st.session_state.predictions_df.set_index("Feature1")["Prediction"])
    else:
        st.write("No predictions yet. Please go to Page 1 and make a prediction.")
