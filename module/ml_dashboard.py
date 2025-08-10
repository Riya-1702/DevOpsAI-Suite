import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random



# Initialize session state
if 'current_section' not in st.session_state:
    st.session_state.current_section = 'dashboard'

# Enhanced sample dataset generation
@st.cache_data
def create_enhanced_dataset(n_samples=150):
    np.random.seed(123)
    random.seed(123)
    
    # More diverse data with realistic correlations
    data = {
        'Employee_Age': np.random.gamma(2, 20, n_samples),  # Gamma distribution for age
        'Annual_Income': np.random.lognormal(10.5, 0.4, n_samples),  # Log-normal for income
        'Years_Experience': np.random.exponential(8, n_samples),  # Exponential for experience
        'Education_Level': [random.choice(['Bachelor', 'Master', 'PhD', 'High School']) for _ in range(n_samples)],
        'Work_Location': [random.choice(['Remote', 'Hybrid', 'Office', 'Field']) for _ in range(n_samples)],
        'Job_Satisfaction': np.random.beta(2, 1, n_samples) * 10,  # Beta distribution scaled to 0-10
        'Productivity_Score': np.random.normal(78, 12, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Add realistic correlations
    df['Annual_Income'] = df['Annual_Income'] + df['Years_Experience'] * 2000 + np.random.normal(0, 5000, n_samples)
    df['Productivity_Score'] = df['Productivity_Score'] + df['Job_Satisfaction'] * 1.5 + np.random.normal(0, 5, n_samples)
    
    # Introduce strategic missing values (15% missing)
    for col in ['Employee_Age', 'Annual_Income', 'Years_Experience']:
        missing_mask = np.random.random(n_samples) < 0.15
        df.loc[missing_mask, col] = np.nan
    
    # Round numerical values
    df['Employee_Age'] = df['Employee_Age'].round(0)
    df['Annual_Income'] = df['Annual_Income'].round(0)
    df['Years_Experience'] = df['Years_Experience'].round(1)
    df['Job_Satisfaction'] = df['Job_Satisfaction'].round(1)
    df['Productivity_Score'] = df['Productivity_Score'].round(1)
    
    return df

def display_missing_value_techniques():
    st.header("🔧 Advanced Missing Data Handling")
    st.markdown("""
    Explore sophisticated imputation strategies for handling missing data in real-world scenarios.
    Each method has different assumptions and use cases.
    """)
    
    df = create_enhanced_dataset()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Dataset Overview")
        st.dataframe(df.head(8), use_container_width=True)
        
        # Missing data statistics
        missing_stats = df.isnull().sum()
        missing_pct = (missing_stats / len(df) * 100).round(2)
        missing_df = pd.DataFrame({
            'Missing Count': missing_stats,
            'Missing %': missing_pct
        })
        st.write("**Missing Data Summary:**")
        st.dataframe(missing_df[missing_df['Missing Count'] > 0])
    
    with col2:
        # Imputation method selection with descriptions
        method_descriptions = {
            "Forward Fill": "Propagates last valid observation forward",
            "Backward Fill": "Uses next valid observation to fill gaps",
            "Linear Interpolation": "Estimates values using linear interpolation",
            "KNN (k=5)": "Uses 5 nearest neighbors for imputation",
            "Iterative (MICE)": "Multiple Imputation by Chained Equations"
        }
        
        selected_method = st.selectbox("🎯 Choose Imputation Strategy:", 
                                     list(method_descriptions.keys()))
        
        st.info(f"**{selected_method}:** {method_descriptions[selected_method]}")
    
    # Apply selected imputation
    numerical_features = ['Employee_Age', 'Annual_Income', 'Years_Experience']
    processed_df = df.copy()
    
    if selected_method == "Forward Fill":
        processed_df[numerical_features] = df[numerical_features].fillna(method='ffill')
    elif selected_method == "Backward Fill":
        processed_df[numerical_features] = df[numerical_features].fillna(method='bfill')
    elif selected_method == "Linear Interpolation":
        processed_df[numerical_features] = df[numerical_features].interpolate(method='linear')
    elif selected_method == "KNN (k=5)":
        imputer = KNNImputer(n_neighbors=5)
        processed_df[numerical_features] = imputer.fit_transform(df[numerical_features])
    elif selected_method == "Iterative (MICE)":
        imputer = IterativeImputer(max_iter=15, random_state=123)
        processed_df[numerical_features] = imputer.fit_transform(df[numerical_features])
    
    # Interactive visualization
    fig = make_subplots(rows=1, cols=2, 
                       subplot_titles=("Before Imputation", "After Imputation"),
                       specs=[[{"secondary_y": False}, {"secondary_y": False}]])
    
    # Before imputation heatmap
    missing_before = df[numerical_features].isnull().astype(int)
    fig.add_trace(go.Heatmap(z=missing_before.values.T, 
                            x=missing_before.index, 
                            y=missing_before.columns,
                            colorscale='Reds',
                            showscale=False), row=1, col=1)
    
    # After imputation heatmap
    missing_after = processed_df[numerical_features].isnull().astype(int)
    fig.add_trace(go.Heatmap(z=missing_after.values.T, 
                            x=missing_after.index, 
                            y=missing_after.columns,
                            colorscale='Reds',
                            showscale=True), row=1, col=2)
    
    fig.update_layout(height=400, title_text=f"Missing Value Pattern - {selected_method}")
    st.plotly_chart(fig, use_container_width=True)

def display_encoding_analysis():
    st.header("🏷️ Categorical Encoding & Feature Engineering")
    st.markdown("""
    Compare different encoding strategies and their impact on model performance.
    """)
    
    df = create_enhanced_dataset().dropna()
    
    # Encoding options
    encoding_methods = {
        "Label Encoding": "Assigns numerical labels (0, 1, 2, ...)",
        "One-Hot (Keep All)": "Creates binary columns for each category",
        "One-Hot (Drop First)": "Drops first category as reference group",
        "Target Encoding": "Encodes based on target variable mean"
    }
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        selected_encoding = st.selectbox("🎨 Encoding Strategy:", list(encoding_methods.keys()))
        st.info(encoding_methods[selected_encoding])
        
        categorical_col = st.selectbox("📝 Categorical Column:", ['Education_Level', 'Work_Location'])
    
    with col2:
        st.subheader("📈 Original Distribution")
        value_counts = df[categorical_col].value_counts()
        fig_dist = px.pie(values=value_counts.values, names=value_counts.index, 
                         title=f"{categorical_col} Distribution")
        st.plotly_chart(fig_dist, use_container_width=True)
    
    # Apply encoding
    encoded_df = df.copy()
    
    if selected_encoding == "Label Encoding":
        encoder = LabelEncoder()
        encoded_df[f'{categorical_col}_Encoded'] = encoder.fit_transform(df[categorical_col])
        encoding_result = encoded_df[[categorical_col, f'{categorical_col}_Encoded']].drop_duplicates()
        
    elif selected_encoding == "One-Hot (Keep All)":
        encoded_data = pd.get_dummies(df[categorical_col], prefix=categorical_col, drop_first=False)
        encoded_df = pd.concat([encoded_df, encoded_data], axis=1)
        encoding_result = encoded_data.head(10)
        
    elif selected_encoding == "One-Hot (Drop First)":
        encoded_data = pd.get_dummies(df[categorical_col], prefix=categorical_col, drop_first=True)
        encoded_df = pd.concat([encoded_df, encoded_data], axis=1)
        encoding_result = encoded_data.head(10)
        
    elif selected_encoding == "Target Encoding":
        target_means = df.groupby(categorical_col)['Productivity_Score'].mean()
        encoded_df[f'{categorical_col}_TargetEncoded'] = df[categorical_col].map(target_means)
        encoding_result = pd.DataFrame({
            categorical_col: target_means.index,
            'Target_Mean': target_means.values
        })
    
    st.subheader("🔍 Encoding Results")
    st.dataframe(encoding_result, use_container_width=True)

def display_model_initialization():
    st.header("⚙️ Model Initialization & Hyperparameters")
    st.markdown("""
    Explore how different initialization strategies affect model convergence and performance.
    """)
    
    df = create_enhanced_dataset().dropna()
    
    # Model configuration
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎛️ Model Configuration")
        model_type = st.selectbox("🤖 Model Type:", 
                                 ["Random Forest", "Gradient Boosting", "Linear Model"])
        
        n_estimators = st.slider("🌳 Number of Estimators:", 10, 200, 100, 10)
        max_depth = st.slider("📏 Max Depth:", 3, 20, 10)
        random_seed = st.slider("🎲 Random Seed:", 1, 1000, 123)
    
    with col2:
        st.subheader("📊 Feature Selection")
        available_features = ['Employee_Age', 'Annual_Income', 'Years_Experience', 'Job_Satisfaction']
        selected_features = st.multiselect("🎯 Input Features:", 
                                         available_features, 
                                         default=available_features[:3])
        
        target_var = st.selectbox("🏆 Target Variable:", ['Productivity_Score'])
    
    if selected_features:
        # Prepare data
        X = df[selected_features]
        y = df[target_var]
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=selected_features)
        
        # Train model
        if model_type == "Random Forest":
            model = RandomForestRegressor(n_estimators=n_estimators, 
                                        max_depth=max_depth, 
                                        random_state=random_seed)
        model.fit(X_scaled, y)
        
        # Model performance
        y_pred = model.predict(X_scaled)
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        
        # Display results
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.metric("📈 R² Score", f"{r2:.3f}")
        with col2:
            st.metric("📉 MSE", f"{mse:.2f}")
        with col3:
            st.metric("🎯 Features", len(selected_features))
        
        # Feature importance visualization
        if hasattr(model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'Feature': selected_features,
                'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=True)
            
            fig_importance = px.bar(importance_df, x='Importance', y='Feature', 
                                  orientation='h', title="Feature Importance")
            st.plotly_chart(fig_importance, use_container_width=True)

def display_advanced_analytics():
    st.header("🧠 Advanced AI Analytics")
    st.markdown("""
    Sophisticated analysis using modern machine learning techniques and interactive visualizations.
    """)
    
    df = create_enhanced_dataset().dropna()
    
    # Analytics options
    analysis_type = st.selectbox("🔬 Analysis Type:", 
                               ["Correlation Analysis", "Performance Clustering", "Predictive Modeling"])
    
    if analysis_type == "Correlation Analysis":
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        correlation_matrix = df[numerical_cols].corr()
        
        fig_corr = px.imshow(correlation_matrix, 
                           title="Feature Correlation Heatmap",
                           color_continuous_scale='RdBu_r',
                           aspect="auto")
        st.plotly_chart(fig_corr, use_container_width=True)
        
    elif analysis_type == "Performance Clustering":
        # Create performance segments
        df['Performance_Segment'] = pd.cut(df['Productivity_Score'], 
                                         bins=3, 
                                         labels=['Low', 'Medium', 'High'])
        
        fig_scatter = px.scatter(df, x='Annual_Income', y='Job_Satisfaction',
                               color='Performance_Segment',
                               size='Years_Experience',
                               title="Performance Clustering Analysis",
                               hover_data=['Employee_Age'])
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    elif analysis_type == "Predictive Modeling":
        # Train-test simulation
        feature_cols = ['Employee_Age', 'Annual_Income', 'Years_Experience', 'Job_Satisfaction']
        X = df[feature_cols]
        y = df['Productivity_Score']
        
        # Add noise for simulation
        X_train = X.sample(frac=0.8, random_state=123)
        X_test = X.drop(X_train.index)
        y_train = y.loc[X_train.index]
        y_test = y.loc[X_test.index]
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=123)
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Prediction vs Actual plot
        pred_df = pd.DataFrame({
            'Actual': y_test,
            'Predicted': y_pred
        })
        
        fig_pred = px.scatter(pred_df, x='Actual', y='Predicted',
                            title="Prediction vs Actual Performance",
                            trendline="ols")
        fig_pred.add_shape(type="line", x0=pred_df['Actual'].min(), 
                          y0=pred_df['Actual'].min(),
                          x1=pred_df['Actual'].max(), 
                          y1=pred_df['Actual'].max(),
                          line=dict(color="red", dash="dash"))
        st.plotly_chart(fig_pred, use_container_width=True)

def display_optimization_playground():
    st.header("⚡ Optimization Playground")
    st.markdown("""
    Interactive exploration of optimization algorithms and their convergence patterns.
    """)
    
    # Optimization parameters
    col1, col2 = st.columns([1, 1])
    
    with col1:
        optimizer_type = st.selectbox("🚀 Optimizer:", 
                                    ["Adam", "SGD", "RMSprop", "AdaGrad"])
        learning_rate = st.slider("📈 Learning Rate:", 0.001, 0.1, 0.01, 0.001)
        epochs = st.slider("🔄 Epochs:", 10, 100, 50, 5)
    
    with col2:
        problem_type = st.selectbox("🎯 Problem Type:", 
                                  ["Quadratic", "Rosenbrock", "Beale"])
        noise_level = st.slider("🔊 Noise Level:", 0.0, 0.5, 0.1, 0.05)
    
    # Simulate optimization curves
    np.random.seed(123)
    x = np.arange(1, epochs + 1)
    
    if optimizer_type == "Adam":
        base_curve = 1 / (0.3 * x**1.2 + 1)
    elif optimizer_type == "SGD":
        base_curve = 1 / (0.1 * x + 1)
    elif optimizer_type == "RMSprop":
        base_curve = 1 / (0.2 * x**1.1 + 1)
    else:  # AdaGrad
        base_curve = 1 / (0.15 * x**0.9 + 1)
    
    # Add noise and learning rate effect
    noise = np.random.normal(0, noise_level, len(x))
    loss_curve = base_curve * (1 / learning_rate) * 0.01 + noise
    loss_curve = np.maximum(loss_curve, 0.001)  # Ensure positive values
    
    # Create interactive plot
    optimization_df = pd.DataFrame({
        'Epoch': x,
        'Loss': loss_curve,
        'Optimizer': optimizer_type
    })
    
    fig_opt = px.line(optimization_df, x='Epoch', y='Loss', 
                     title=f"{optimizer_type} Optimization Curve",
                     markers=True)
    fig_opt.update_layout(yaxis_type="log")
    st.plotly_chart(fig_opt, use_container_width=True)
    
    # Convergence metrics
    final_loss = loss_curve[-1]
    convergence_rate = (loss_curve[0] - loss_curve[-1]) / loss_curve[0]
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.metric("🎯 Final Loss", f"{final_loss:.4f}")
    with col2:
        st.metric("📉 Convergence Rate", f"{convergence_rate:.2%}")
    with col3:
        st.metric("⏱️ Total Epochs", epochs)

def run():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">🚀 AI/ML Analytics Hub</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            Advanced Machine Learning Analytics with Interactive Visualizations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation with enhanced styling
    with st.sidebar:
        st.markdown("### 🧭 Navigation Hub")
        
        sections = {
            "🏠 Dashboard": "dashboard",
            "🔧 Data Imputation": "imputation", 
            "🏷️ Encoding Analysis": "encoding",
            "⚙️ Model Init": "initialization",
            "🧠 AI Analytics": "analytics",
            "⚡ Optimization": "optimization"
        }
        
        selected_section = st.radio("Choose Section:", list(sections.keys()))
        st.session_state.current_section = sections[selected_section]
        
        # Dataset info
        st.markdown("---")
        st.markdown("### 📊 Dataset Info")
        df = create_enhanced_dataset()
        st.metric("📈 Samples", len(df))
        st.metric("📋 Features", len(df.columns))
        st.metric("🔍 Missing %", f"{(df.isnull().sum().sum() / df.size * 100):.1f}%")
    
    # Main content routing
    if st.session_state.current_section == 'dashboard':
        # Dashboard overview
        st.markdown("### 🎯 Welcome to the Analytics Hub")
        
        # Quick stats
        df = create_enhanced_dataset()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Employees", len(df), delta="150 samples")
        with col2:
            avg_income = df['Annual_Income'].mean()
            st.metric("💰 Avg Income", f"${avg_income:,.0f}", delta="5.2%")
        with col3:
            avg_satisfaction = df['Job_Satisfaction'].mean()
            st.metric("😊 Satisfaction", f"{avg_satisfaction:.1f}/10", delta="0.3")
        with col4:
            avg_productivity = df['Productivity_Score'].mean()
            st.metric("📈 Productivity", f"{avg_productivity:.1f}", delta="2.1")
        
        # Dataset preview
        st.markdown("### 📋 Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Quick visualization
        st.markdown("### 📊 Quick Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(df, x='Education_Level', 
                              title="Education Distribution")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.box(df, x='Work_Location', y='Job_Satisfaction',
                         title="Satisfaction by Work Location")
            st.plotly_chart(fig2, use_container_width=True)
        
    elif st.session_state.current_section == 'imputation':
        display_missing_value_techniques()
    elif st.session_state.current_section == 'encoding':
        display_encoding_analysis()
    elif st.session_state.current_section == 'initialization':
        display_model_initialization()
    elif st.session_state.current_section == 'analytics':
        display_advanced_analytics()
    elif st.session_state.current_section == 'optimization':
        display_optimization_playground()

if __name__ == "__main__":
    run()
