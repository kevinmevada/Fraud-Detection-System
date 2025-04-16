import streamlit as st
import pandas as pd
import numpy as np
import time
import sqlite3
import bcrypt
import plotly.express as px
from fraud_detection import detect_fraud, analyze_behavior_deep, update_model
from data_processor import load_data, process_real_time

# ----------------------------- Theme Styling ----------------------------- #
def apply_cyberpunk_theme():
    st.markdown("""
        <style>
        /* App background & fonts */
        .stApp {
            background: #0A0A0A;
            color: #E0E0E0;
            font-family: 'Poppins', sans-serif;
        }
        /* Sidebar */
        .css-1d391kg {
            background: rgba(20, 20, 20, 0.7);
            color: #E0E0E0;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(0, 198, 255, 0.2);
            backdrop-filter: blur(8px);
        }
        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #00C6FF, #0072FF);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
            font-size: 16px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: background 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #0072FF, #00C6FF);
        }
        /* Titles */
        h1, h2, h3 {
            color: #00C6FF;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 700;
            margin-bottom: 15px;
        }
        /* Cards */
        .stCard {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(0, 198, 255, 0.2);
            backdrop-filter: blur(6px);
            margin: 10px 0;
        }
        /* Text Inputs */
        .stTextInput>div>div>input {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(0, 198, 255, 0.3);
            color: #E0E0E0;
            border-radius: 8px;
            padding: 10px;
            font-size: 15px;
        }
        .stTextInput>div>div>input:focus {
            border-color: #00C6FF;
        }
        /* Tabs */
        .stTabs [data-baseweb="tab"] {
            font-size: 15px;
            color: #E0E0E0;
            padding: 8px 15px;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: #00C6FF;
            border-bottom: 2px solid #00C6FF;
        }
        /* Misc */
        .main .block-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        @media (max-width: 600px) {
            .stButton>button { padding: 10px 15px; font-size: 14px; }
            .stCard { padding: 10px; }
        }
        </style>
    """, unsafe_allow_html=True)

# ----------------------------- Initialization ----------------------------- #
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

apply_cyberpunk_theme()

# ----------------------------- User Authentication ----------------------------- #
def init_users_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (username TEXT PRIMARY KEY, password BLOB)''')
    conn.commit()
    conn.close()

def add_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_password(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    stored = c.fetchone()
    conn.close()
    return bcrypt.checkpw(password.encode('utf-8'), stored[0]) if stored else False

init_users_db()

# ----------------------------- App Layout ----------------------------- #
st.title("Fraud Detection System")
st.markdown("<h3>Secure Transactions, Made Simple</h3>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown("<p style='text-align: center;'>Sign in or create an account to get started.</p>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])

    with tab1:
        login_username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        login_password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
        if st.button("Sign In", key="login_btn"):
            if verify_password(login_username, login_password):
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.success("Signed in successfully.")
            else:
                st.error("Incorrect username or password.")

    with tab2:
        signup_username = st.text_input("New Username", key="signup_username", placeholder="Choose a username")
        signup_password = st.text_input("New Password", type="password", key="signup_password", placeholder="Choose a password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password", placeholder="Confirm your password")
        if st.button("Create Account", key="signup_btn"):
            if signup_password != confirm_password:
                st.error("Passwords do not match.")
            elif len(signup_password) < 6:
                st.error("Password must be at least 6 characters.")
            elif add_user(signup_username, signup_password):
                st.success("Account created. Please sign in.")
            else:
                st.error("Username already taken.")
else:
    st.markdown(f"<div class='stCard'><p style='text-align: center;'>Welcome, {st.session_state.username}</p></div>", unsafe_allow_html=True)

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Choose an option", [
        "Machine Learning Analysis",
        "Real-Time Monitoring",
        "Behavioral Pattern Analysis",
        "Interactive Dashboard",
        "Historical Data Utilization",
        "Scalability Settings"
    ])

    if st.sidebar.button("Sign Out", key="logout_btn"):
        st.session_state.clear()
        st.success("Signed out successfully.")

    # Settings
    st.sidebar.header("Settings")
    threshold = st.sidebar.slider("Fraud Detection Threshold", 0.0, 1.0, 0.001, help="Adjust sensitivity.")
    custom_threshold = st.sidebar.text_input("Custom Threshold", "0.001", placeholder="Enter a value between 0 and 1")
    if st.sidebar.button("Apply Settings", key="apply_btn"):
        try:
            update_model(float(custom_threshold))
            st.sidebar.success("Settings applied.")
        except ValueError:
            st.sidebar.error("Please enter a valid number.")

    # Data Load
    try:
        data = load_data()
        historical_data = data.copy()
    except Exception as e:
        st.error(f"Data loading failed: {e}")
        data = pd.DataFrame()
        historical_data = pd.DataFrame()

    # ----------------------------- Main Dashboard Views ----------------------------- #
    if choice == "Machine Learning Analysis":
        st.header("Machine Learning Analysis")
        st.write("Employs unsupervised learning to detect anomalies.")
        if st.button("Analyze Data", key="analyze_btn"):
            if not data.empty:
                frauds = detect_fraud(historical_data, threshold)
                st.write(f"Detected {len(frauds)} fraudulent transactions.")
                fig = px.line(frauds, y='anomaly_score', title="Anomaly Scores", color_discrete_sequence=['#00C6FF'])
                st.plotly_chart(fig, use_container_width=True)

    elif choice == "Real-Time Monitoring":
        st.header("Real-Time Monitoring")
        st.write("Analyzes transactions in real-time.")
        if st.button("Start Monitoring", key="rt_btn"):
            if not data.empty:
                for _ in range(5):
                    new_data = process_real_time(data)
                    frauds_rt = detect_fraud(new_data, threshold)
                    st.write(f"Detected {len(frauds_rt)} frauds in real-time.")
                    if not frauds_rt.empty:
                        st.dataframe(frauds_rt, use_container_width=True)
                        st.warning("Suspicious activity detected!")
                    time.sleep(2)
            else:
                st.error("No data available.")

    elif choice == "Behavioral Pattern Analysis":
        st.header("Behavioral Pattern Analysis")
        st.write("Tracks user behavior for anomalies.")
        if not data.empty:
            behavior = analyze_behavior_deep(data)
            st.dataframe(behavior, use_container_width=True)
        else:
            st.error("No data available.")

    elif choice == "Interactive Dashboard":
        st.header("Interactive Dashboard")
        st.write("Visualizes fraud trends.")
        if st.button("View Dashboard", key="dashboard_btn"):
            if not data.empty:
                frauds = detect_fraud(historical_data, threshold)
                fig1 = px.bar(frauds, y='Amount', title="Transaction Amounts", color_discrete_sequence=['#00C6FF'])
                st.plotly_chart(fig1, use_container_width=True)

                st.write("Correlation Heatmap")
                corr = frauds[['Time', 'Amount']].corr()
                fig2 = px.imshow(corr, text_auto=True, color_continuous_scale=['#0A0A0A', '#00C6FF'], title="Time vs. Amount Correlation")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.error("No data available.")

    elif choice == "Historical Data Utilization":
        st.header("Historical Data Utilization")
        st.write("Leverages past data for insight.")
        if not data.empty:
            st.write(f"Total historical transactions: {len(historical_data)}")
            fig = px.line(historical_data, x='Time', y='Amount', title="Historical Transaction Trends", color_discrete_sequence=['#00C6FF'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No data available.")

    elif choice == "Scalability Settings":
        st.header("Scalability and Customization")
        try:
            conn = sqlite3.connect('transactions.db')
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM transactions')
            row_count = c.fetchone()[0]
            conn.close()
            st.write(f"Stored transactions in SQLite: {row_count}")
        except Exception as e:
            st.error(f"Failed to query database: {e}")
        st.write("Adjust threshold to customize detection.")

    # ----------------------------- SQLite Storage ----------------------------- #
    try:
        conn = sqlite3.connect('transactions.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS transactions
                    (id INTEGER PRIMARY KEY, time REAL, amount REAL, class INTEGER)''')
        data.to_sql('transactions', conn, if_exists='replace', index=False)
        conn.close()
        st.write("Data stored successfully in SQLite.")
    except Exception as e:
        st.error(f"Storage failed: {e}")
