
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Initialize session state
if 'ml_page' not in st.session_state:
    st.session_state.ml_page = 'home'

# Generate sample dataset
@st.cache_data
def generate_sample_data(n_samples=100):
    np.random.seed(42)
    random.seed(42)
    
    # Numerical columns with some missing values
    data = {
        'Age': np.random.normal(40, 10, n_samples),
        'Salary': np.random.normal(50000, 15000, n_samples),
        'Experience': np.random.normal(10, 5, n_samples),
        # Categorical column
        'Department': [random.choice(['HR', 'IT', 'Sales', 'Marketing']) for _ in range(n_samples)],
        # Target variable for regression
        'Performance': np.random.normal(75, 10, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Introduce missing values (10% missing in numerical columns)
    for col in ['Age', 'Salary', 'Experience']:
        mask = np.random.random(n_samples) < 0.1
        df.loc[mask, col] = np.nan
    
    return df

def show_imputation():
    st.header("🧩 Data Imputation Techniques")
    st.markdown("""
    Data imputation handles missing values in datasets. Below, we apply different imputation methods to the generated dataset.
    """)
    
    df = generate_sample_data()
    st.subheader("Sample Dataset with Missing Values")
    st.write(df.head(10))
    
    # Imputation Method Selection
    imputation_method = st.selectbox("Select Imputation Method:", 
                                    ["Mean", "Median", "Mode", "KNN", "MICE"])
    
    numerical_cols = ['Age', 'Salary', 'Experience']
    imputed_df = df.copy()
    
    if imputation_method == "Mean":
        imputer = SimpleImputer(strategy='mean')
        imputed_df[numerical_cols] = imputer.fit_transform(df[numerical_cols])
        st.write("Mean Imputation Result:")
        st.write(imputed_df.head(10))
    elif imputation_method == "Median":
        imputer = SimpleImputer(strategy='median')
        imputed_df[numerical_cols] = imputer.fit_transform(df[numerical_cols])
        st.write("Median Imputation Result:")
        st.write(imputed_df.head(10))
    elif imputation_method == "Mode":
        imputer = SimpleImputer(strategy='most_frequent')
        imputed_df[numerical_cols] = imputer.fit_transform(df[numerical_cols])
        st.write("Mode Imputation Result:")
        st.write(imputed_df.head(10))
    elif imputation_method == "KNN":
        imputer = KNNImputer(n_neighbors=3)
        imputed_df[numerical_cols] = imputer.fit_transform(df[numerical_cols])
        st.write("KNN Imputation Result:")
        st.write(imputed_df.head(10))
    elif imputation_method == "MICE":
        imputer = IterativeImputer(max_iter=10, random_state=42)
        imputed_df[numerical_cols] = imputer.fit_transform(df[numerical_cols])
        st.write("MICE Imputation Result:")
        st.write(imputed_df.head(10))
    
    # Visualize missing values before and after
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    sns.heatmap(df[numerical_cols].isnull(), cbar=False, ax=ax1)
    ax1.set_title("Missing Values Before Imputation")
    sns.heatmap(imputed_df[numerical_cols].isnull(), cbar=False, ax=ax2)
    ax2.set_title("Missing Values After Imputation")
    st.pyplot(fig)

def show_categorical_weight():
    st.header("⚖️ Dropped Category Weight in Categorical Variables")
    st.markdown("""
    One-hot encoding transforms categorical variables. Dropping a category makes it the reference group.
    """)
    
    df = generate_sample_data()
    st.subheader("Sample Dataset (Department Column)")
    st.write(df[['Department']].head(10))
    
    # One-hot encoding with drop option
    drop_option = st.checkbox("Drop first category (HR)", value=True)
    encoder = OneHotEncoder(drop='first' if drop_option else None, sparse_output=False)
    encoded_data = encoder.fit_transform(df[['Department']])
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(['Department']))
    
    st.write("Encoded Data:")
    st.write(encoded_df.head(10))
    
    # Demonstrate effect on regression
    st.subheader("Effect on Linear Regression")
    X = encoded_df
    y = df['Performance']
    model = LinearRegression().fit(X, y)
    coef_df = pd.DataFrame({
        'Feature': encoder.get_feature_names_out(['Department']),
        'Coefficient': model.coef_
    })
    st.write("Regression Coefficients (relative to dropped category if checked):")
    st.write(coef_df)

def show_initializers():
    st.header("🔬 Initializers in ML")
    st.markdown("""
    Initializers set starting weights in neural networks. We visualize their distributions using the generated dataset's scale.
    """)
    
    df = generate_sample_data()
    salary_std = df['Salary'].std()
    
    initializers = ['Zeros', 'Ones', 'Random Normal', 'Glorot Uniform', 'He Uniform']
    selected_initializer = st.selectbox("Select Initializer:", initializers)
    
    # Simulate weight distribution
    np.random.seed(42)
    weights = []
    if selected_initializer == 'Zeros':
        weights = np.zeros(1000)
    elif selected_initializer == 'Ones':
        weights = np.ones(1000)
    elif selected_initializer == 'Random Normal':
        weights = np.random.normal(0, salary_std / 1000, 1000)
    elif selected_initializer == 'Glorot Uniform':
        weights = np.random.uniform(-np.sqrt(6/2) * salary_std / 1000, np.sqrt(6/2) * salary_std / 1000, 1000)
    elif selected_initializer == 'He Uniform':
        weights = np.random.uniform(-np.sqrt(6/1) * salary_std / 1000, np.sqrt(6/1) * salary_std / 1000, 1000)
    
    # Plot distribution
    fig, ax = plt.subplots()
    sns.histplot(weights, bins=30, ax=ax)
    ax.set_title(f"{selected_initializer} Distribution (Scaled by Salary Std)")
    st.pyplot(fig)

def show_llm():
    st.header("🧠 LLM Model Structure & API")
    st.markdown("""
    LLMs process text data. Below is a mock sentiment analysis on the generated dataset's department names.
    """)
    
    df = generate_sample_data()
    st.subheader("Sample Department Data")
    st.write(df[['Department']].head(10))
    
    st.markdown("Enter a department name for mock sentiment analysis:")
    user_input = st.text_input("Department:", "IT")
    
    # Mock sentiment analysis (since actual LLM requires local execution)
    sentiment_map = {'HR': 'Neutral', 'IT': 'Positive', 'Sales': 'Positive', 'Marketing': 'Neutral'}
    sentiment = sentiment_map.get(user_input, "Neutral")
    st.write(f"Sentiment Analysis Result for '{user_input}': {sentiment}")
    
    st.markdown("**Code Example for Actual LLM Usage**:")
    st.code("""
    from transformers import pipeline
    nlp = pipeline("sentiment-analysis")
    result = nlp("IT")
    print(result)
    """, language="python")

def show_optimizers():
    st.header("⚡ Optimizers in ML")
    st.markdown("""
    Optimizers update model weights. We simulate training a linear regression model on the generated dataset.
    """)
    
    df = generate_sample_data()
    df = df.dropna()  # Remove missing values for simplicity
    X = df[['Age', 'Salary', 'Experience']]
    y = df['Performance']
    
    optimizers = ['SGD', 'Adam', 'RMSprop']
    selected_optimizer = st.selectbox("Select Optimizer:", optimizers)
    
    # Simulate loss curves (mock optimization)
    np.random.seed(42)
    epochs = np.arange(1, 11)
    if selected_optimizer == 'SGD':
        loss = 1 / (0.1 * epochs)
    elif selected_optimizer == 'Adam':
        loss = 1 / (0.2 * epochs**1.5)
    elif selected_optimizer == 'RMSprop':
        loss = 1 / (0.15 * epochs**1.2)
    
    # Plot loss curve
    fig, ax = plt.subplots()
    ax.plot(epochs, loss, label=selected_optimizer)
    ax.set_xlabel("Epochs")
    ax.set_ylabel("Loss")
    ax.set_title(f"{selected_optimizer} Loss Curve (Mock)")
    ax.legend()
    st.pyplot(fig)
    
    # Train a simple linear regression as a demo
    model = LinearRegression().fit(X, y)
    st.write("Linear Regression R² Score on Dataset:")
    st.write(f"{model.score(X, y):.4f}")

def show_activation_pooling():
    st.header("🔗 Activation Functions & Pooling")
    st.markdown("""
    Activation functions introduce non-linearity. We visualize them using the generated dataset's scale.
    """)
    
    df = generate_sample_data()
    salary_range = df['Salary'].max() - df['Salary'].min()
    
    activations = ['ReLU', 'Sigmoid', 'Tanh']
    selected_activation = st.selectbox("Select Activation Function:", activations)
    
    # Simulate activation function
    x = np.linspace(-salary_range / 100, salary_range / 100, 100)
    if selected_activation == 'ReLU':
        y = np.maximum(0, x)
    elif selected_activation == 'Sigmoid':
        y = 1 / (1 + np.exp(-x))
    elif selected_activation == 'Tanh':
        y = np.tanh(x)
    
    # Plot activation function
    fig, ax = plt.subplots()
    ax.plot(x, y, label=selected_activation)
    ax.set_xlabel("Input (Scaled by Salary Range)")
    ax.set_ylabel("Output")
    ax.set_title(f"{selected_activation} Activation Function")
    ax.legend()
    st.pyplot(fig)

def run():
    st.title("🤖 ML Mini Dashboard with Generated Data")
    st.markdown("Welcome to the Machine Learning Dashboard! This uses a randomly generated dataset.")
    
    # Display sample dataset
    st.subheader("📊 Generated Dataset")
    df = generate_sample_data()
    st.write(df.head(10))
    st.write(f"Dataset Shape: {df.shape}")
    
    # Display available ML modules
    st.subheader("📊 Available ML Modules")
    ml_modules = [
        {
            "name": "📈 ML Regression",
            "description": "Advanced regression analysis with data visualization and machine learning models",
            "status": "✅ Available"
        }
    ]
    
    for module in ml_modules:
        with st.expander(f"{module['name']} - {module['status']}"):
            st.write(module['description'])
            st.info("Select this module from the sidebar to access it directly.")
    
    st.markdown("---")
    st.markdown("### 🎯 How to Use")
    st.markdown("""
    1. **Choose a Module**: Select any ML module from the sidebar navigation
    2. **Explore Features**: Each module applies techniques to the generated dataset
    3. **Interact**: Use dropdowns and checkboxes to explore different methods
    4. **View Results**: See visualizations and results tailored to the dataset
    """)

    with st.sidebar:
        page = st.radio(
            "Select ML Topic:",
            ["🏠 Home", "🧩 Imputation", "⚖️ Categorical Weight", "🔬 Initializers", "🧠 LLM", "⚡ Optimizers", "🔗 Activation/Pooling"],
            index=0
        )
        if page == "🏠 Home":
            st.session_state.ml_page = 'home'
        elif page == "🧩 Imputation":
            st.session_state.ml_page = 'imputation'
        elif page == "⚖️ Categorical Weight":
            st.session_state.ml_page = 'catweight'
        elif page == "🔬 Initializers":
            st.session_state.ml_page = 'initializers'
        elif page == "🧠 LLM":
            st.session_state.ml_page = 'llm'
        elif page == "⚡ Optimizers":
            st.session_state.ml_page = 'optimizers'
        elif page == "🔗 Activation/Pooling":
            st.session_state.ml_page = 'activationpooling'
    
    if st.session_state.ml_page == 'imputation':
        show_imputation()
    elif st.session_state.ml_page == 'catweight':
        show_categorical_weight()
    elif st.session_state.ml_page == 'initializers':
        show_initializers()
    elif st.session_state.ml_page == 'llm':
        show_llm()
    elif st.session_state.ml_page == 'optimizers':
        show_optimizers()
    elif st.session_state.ml_page == 'activationpooling':
        show_activation_pooling()

# Function to be called by app.py
def run():
    # Main dashboard code
    st.title("🤖 Machine Learning Dashboard")
    st.markdown("""
    This dashboard demonstrates various machine learning concepts and techniques.
    Choose a topic from the sidebar to explore different aspects of ML.
    """)
    
    # Sidebar navigation
    page = st.sidebar.radio(
        "📊 Choose a Topic",
        ["🏠 Home", "🧩 Data Imputation", "🔢 Categorical & Weight", "🎲 Initializers", 
         "🧠 LLM", "⚡ Optimizers", "🔗 Activation/Pooling"]
    )
    
    if page == "🏠 Home":
        st.session_state.ml_page = 'home'
    elif page == "🧩 Data Imputation":
        st.session_state.ml_page = 'imputation'
    elif page == "🔢 Categorical & Weight":
        st.session_state.ml_page = 'catweight'
    elif page == "🎲 Initializers":
        st.session_state.ml_page = 'initializers'
    elif page == "🧠 LLM":
        st.session_state.ml_page = 'llm'
    elif page == "⚡ Optimizers":
        st.session_state.ml_page = 'optimizers'
    elif page == "🔗 Activation/Pooling":
        st.session_state.ml_page = 'activationpooling'
    
    if st.session_state.ml_page == 'imputation':
        show_imputation()
    elif st.session_state.ml_page == 'catweight':
        show_categorical_weight()
    elif st.session_state.ml_page == 'initializers':
        show_initializers()
    elif st.session_state.ml_page == 'llm':
        show_llm()
    elif st.session_state.ml_page == 'optimizers':
        show_optimizers()
    elif st.session_state.ml_page == 'activationpooling':
        show_activation_pooling()

if __name__ == "__main__":
    run()