# **Fraud Detection System**

A sleek, **Cyberpunk-themed Streamlit application** for detecting fraudulent transactions using machine learning, real-time monitoring, and behavioral analysis. Built for scalability and interactive insights, this project leverages historical and real-time data to empower informed decision-making.

---

## 🚀 Features

- **🧠 Machine Learning Analysis**  
  Uses unsupervised learning (`IsolationForest`) to detect anomalies, adapting to emerging fraud patterns.

- **⏱️ Real-Time Monitoring**  
  Analyzes transactions in real-time, instantly alerting suspicious activity.

- **👤 Behavioral Pattern Analysis**  
  Tracks user behavior to identify unusual patterns and distinguish between normal and fraudulent activities.

- **📊 Interactive Dashboard**  
  Visualizes fraud trends and transaction patterns with large, easy-to-read charts.

- **🕰 Historical Data Utilization**  
  Combines past transaction data with real-time activity for powerful predictive insights.

- **⚙️ Scalability & Customization**  
  Handles large-scale data and allows dynamic adjustment of fraud detection thresholds.

---

## 🖥 Demo Design

- **Theme:** Cyberpunk  
- **Background:** `#0A0A0A`  
- **Accents:** Cyan `#00C6FF`, Blue `#0072FF`  
- **Font:** Poppins  
- **Graphs:** 600px height × 900px width

---

## 🔧 Prerequisites

- Python 3.8+
- Libraries: `streamlit`, `pandas`, `numpy`, `scikit-learn`, `bcrypt`, `plotly`

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/kevinmevada/fraud-detection-system.git
cd fraud-detection-system

# Set up a virtual environment
python -m venv venv

# Activate the environment
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Install dependencies
pip install streamlit pandas numpy scikit-learn bcrypt plotly
```

> 📥 **Note**: Download `creditcard.csv` dataset from Kaggle and place it in the project root.

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Open your browser and visit: [http://localhost:8501](http://localhost:8501)

---

## 👤 Usage

- **Sign Up**: Create an account (username + password with minimum 6 characters).
- **Sign In**: Log in using your credentials.
- **Explore**: Use the sidebar to navigate between:
  - Machine Learning Analysis
  - Real-Time Monitoring
  - Behavioral Insights
- **Settings**: Adjust detection sensitivity threshold.
- **Sign Out**: End your session securely.

---

## 📁 Project Structure

```
fraud_detection_project/
├── app.py              # Main Streamlit app with Cyberpunk UI
├── data_processor.py   # Data loading and real-time simulation
├── fraud_detection.py  # Machine learning and behavioral analysis
├── creditcard.csv      # Dataset (user-provided)
├── transactions.db     # SQLite DB for transactions
├── users.db            # SQLite DB for user credentials
```

---

## 🤝 Contributing

1. Fork the repository  
2. Create your feature branch  
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes  
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to GitHub  
   ```bash
   git push origin feature-name
   ```
5. Submit a Pull Request 🚀

---

## 📜 License

Feel free to modify and distribute.

---

## 📬 Contact

For questions or support, feel free to reach out:

**Kevin Mevada**  
📧 [mevadakevin@gmail.com](mailto:mevadakevin@gmail.com)  
🔗 [github.com/kevinmevada](https://github.com/kevinmevada)
