def run():
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    import os  # <-- 1. Import the os module

    # 2. Build the full path to the data file
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "temp_data.csv")

    st.title("🌡️ Temperature Prediction")
    st.sidebar.header("Enter Weather Details")
    
    # --- Sidebar Inputs (No changes here) ---
    humidity = st.sidebar.slider("Humidity (%)", 0, 100)
    wind_speed = st.sidebar.slider("Wind Speed (km/h)", 0, 50)
    previous_temp = st.sidebar.number_input("Previous Day Temp (°C)", min_value=0.0, max_value=50.0)
    
    if st.sidebar.button("Submit"):
        st.write("Input Summary")
        st.write(f"Humidity: {humidity}%")
        st.write(f"Wind Speed: {wind_speed} km/h")
        st.write(f"Previous Temperature: {previous_temp} °C")
    
    try:
        # 3. Use the full file_path to read the CSV
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Data file not found. Make sure 'temp_data.csv' is in the 'module' folder.")
        st.stop() # Stop the app if the data can't be loaded

    # --- Model Training and Prediction (No changes here) ---
    x = df[["Humidity", "Wind_Speed", "Previous_Temp"]]
    y = df["Today_Temp"]
    p = LinearRegression()
    p.fit(x, y)
    predicted_temp = p.predict([[humidity, wind_speed, previous_temp]])
    
    if st.button("Predict"):
        st.success(f"Predicted Today's Temperature: {predicted_temp[0]:.2f} °C")

    # --- Graphing and Download (No changes here) ---
    st.header("📊 View Historical Data Graph?")
    if st.button("Yes"):
        st.subheader("Temperature vs Humidity and Wind Speed")
        fig, ax = plt.subplots()
        scatter = ax.scatter(df["Humidity"], df["Wind_Speed"], c=df["Today_Temp"], cmap='coolwarm', s=100)
        ax.set_xlabel("Humidity (%)")
        ax.set_ylabel("Wind Speed (km/h)")
        cbar = plt.colorbar(scatter)
        cbar.set_label("Today Temp (°C)")
        st.pyplot(fig)
        
    result_df = pd.DataFrame({
        "Humidity": [humidity],
        "Wind Speed": [wind_speed],
        "Previous Temp": [previous_temp],
        "Predicted Temp": [predicted_temp[0]]
    })
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Prediction as CSV", data=csv, file_name="prediction.csv", mime="text/csv")