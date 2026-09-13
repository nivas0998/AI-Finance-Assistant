# 💰 AI Finance Assistant

An AI-powered personal finance management application that helps users record, categorize, analyze, and understand their income and expenses.

The project combines **React, FastAPI, SQLite, and Machine Learning** to provide a beginner-friendly finance assistant with expense categorization, budgeting, spending analysis, forecasting, financial insights, and an interactive chatbot.

> **Disclaimer:** This project is developed for educational and portfolio purposes. It does not provide professional financial, investment, tax, or banking advice.

---

## 🚀 Features

### 🔐 User Authentication

* User registration
* User login
* Password hashing using bcrypt
* User-specific financial data
* Input validation

### 💸 Transaction Management

* Add income and expense transactions
* View transaction history
* Delete transactions
* Categorize transactions
* Store transaction date, description, amount, type, and category

### 🤖 AI Expense Categorization

The application uses Machine Learning to automatically predict an expense category from its description.

Supported categories:

* Food
* Transport
* Shopping
* Bills
* Entertainment
* Health
* Education
* Other

The model uses:

* TF-IDF text vectorization
* Logistic Regression
* Prediction probability for confidence estimation

Users can also manually select or correct a category.

### 📊 Dashboard & Analytics

The dashboard provides:

* Total income
* Total expenses
* Current balance
* Category-wise expense visualization
* Transaction history
* Spending summaries
* Monthly financial information

Charts are implemented using Recharts.

### 💰 Budget Management

Users can:

* Create monthly budgets
* Set category-wise limits
* View budget information
* Compare spending with budget limits
* Monitor budget usage

### 🧠 AI Financial Insights

The system generates simple insights based on recorded financial data, including:

* High spending categories
* Income vs expense comparison
* Budget-related observations
* Basic spending suggestions
* Positive financial observations

### 📈 Spending Forecast

The application provides a basic prediction of future spending using historical expense data.

The forecasting module uses:

* Monthly expense aggregation
* Linear Regression
* Historical spending information
* Basic model evaluation

Forecasts are estimates and are not guaranteed financial predictions.

### 💬 Finance Chatbot

The built-in Finance Assistant allows users to ask questions about their recorded financial information.

Example questions:

```text
How much did I spend?
What is my balance?
What is my highest spending category?
How much income did I record?
How many transactions do I have?
Give me a saving tip.
```

The chatbot retrieves the user's recorded data from the database and generates simple responses.

---

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* JavaScript
* React Router
* Axios
* Recharts
* Lucide React
* Framer Motion
* CSS

### Backend

* Python
* FastAPI
* Uvicorn
* SQLite
* bcrypt
* Pydantic

### Machine Learning

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib
* TF-IDF
* Logistic Regression
* Linear Regression

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │       React UI      │
                    │      Frontend       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI         │
                    │    Backend API      │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
          ┌───────────┐ ┌────────────┐ ┌─────────────┐
          │ Validation│ │  SQLite DB │ │ ML Modules  │
          └───────────┘ └────────────┘ └──────┬──────┘
                                               │
                            ┌──────────────────┼─────────────────┐
                            │                  │                 │
                            ▼                  ▼                 ▼
                     ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
                     │   Expense   │   │  Spending   │   │  Financial  │
                     │Categorization│   │  Forecast   │   │   Insights  │
                     └─────────────┘   └─────────────┘   └─────────────┘
                                               │
                                               ▼
                                      ┌────────────────┐
                                      │ Finance Chatbot│
                                      └────────────────┘
```

---

## 📁 Project Structure

```text
AI-Finance-Assistant/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   └── chatbot.py
│
├── ml/
│   ├── train_model.py
│   ├── predict.py
│   ├── forecast.py
│   └── expense_category_model.joblib
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── CursorGlow.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── Dashboard.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── screenshots/
│
├── .gitignore
└── README.md
```

---

## 🔌 API Endpoints

### Authentication

```text
POST /register
POST /login
```

### Transactions

```text
POST   /transactions
GET    /transactions/{user_id}
PUT    /transactions/{transaction_id}
DELETE /transactions/{transaction_id}
```

### AI Expense Prediction

```text
POST /predict-category
```

### Dashboard

```text
GET /dashboard/{user_id}
```

### Budgets

```text
POST /budgets
GET  /budgets/{user_id}
GET  /budgets/{user_id}/status
```

### Financial Insights

```text
GET /insights/{user_id}
```

### Spending Forecast

```text
GET /forecast/{user_id}
```

### Finance Chatbot

```text
POST /chat
```

---

## 🧠 Machine Learning

### Expense Classification

The expense classification pipeline uses textual transaction descriptions.

Example:

```text
Description: "ordered pizza"
Prediction: Food
```

```text
Description: "Uber ride"
Prediction: Transport
```

```text
Description: "Amazon shopping"
Prediction: Shopping
```

The pipeline performs:

```text
Transaction Description
        ↓
Text Preprocessing
        ↓
TF-IDF Vectorization
        ↓
Logistic Regression
        ↓
Predicted Category
        ↓
Confidence Score
```

### Spending Forecast

Historical monthly expense data is used to estimate the next month's spending.

```text
Historical Expenses
        ↓
Monthly Aggregation
        ↓
Linear Regression
        ↓
Future Spending Estimate
```

The forecast requires sufficient historical data. When insufficient data is available, the application informs the user instead of producing an unreliable prediction.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/nivas0998/AI-Finance-Assistant.git
```

```bash
cd AI-Finance-Assistant
```

---

## 🐍 Backend Setup

Create a virtual environment:

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Install dependencies:

```powershell
python -m pip install fastapi uvicorn sqlalchemy pymysql python-dotenv python-multipart email-validator bcrypt
```

Install Machine Learning dependencies:

```powershell
python -m pip install pandas numpy scikit-learn joblib
```

---

## 🤖 Train the ML Model

From the project root:

```powershell
python ml/train_model.py
```

This creates:

```text
ml/expense_category_model.joblib
```

---

## ▶️ Start the Backend

Run:

```powershell
python -m uvicorn backend.main:app --reload
```

Backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## ⚛️ Frontend Setup

Open another terminal:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

Vite will provide the local frontend URL in the terminal.

---

## 🗄️ Database

The project uses **SQLite** for simple local development and educational use.

The database contains tables for:

```text
users
transactions
budgets
```

The database file is intentionally excluded from Git using:

```text
finance.db
```

in `.gitignore`.

---

## 🔒 Security

The application includes basic security practices:

* Password hashing using bcrypt
* Input validation using Pydantic
* User-specific financial records
* Database constraints
* Sensitive database files excluded from Git
* `.env` files excluded from Git
* No passwords stored as plain text

For production deployment, HTTPS, stronger authentication/session management, secure secrets management, and additional authorization controls should be implemented.

---

## 🧪 Testing

The following major features have been tested during development:

* User registration
* User login
* Transaction creation
* Transaction retrieval
* Transaction deletion
* AI expense categorization
* Budget creation
* Dashboard calculations
* AI financial insights
* Spending forecast
* Finance chatbot
* Frontend-backend API communication

---

## 📸 Screenshots

Add project screenshots inside the `screenshots/` directory.

Recommended screenshots:

```text
screenshots/
├── home.png
├── login.png
├── register.png
├── dashboard.png
├── ai-category.png
├── budget.png
├── insights.png
├── forecast.png
└── chatbot.png
```

Example Markdown:

```markdown
![Dashboard](screenshots/dashboard.png)
```

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Develop a personal finance management application.
2. Provide CRUD operations for financial transactions.
3. Automatically categorize expenses using Machine Learning.
4. Help users monitor budgets.
5. Visualize financial information using charts.
6. Generate simple AI-assisted financial insights.
7. Provide basic spending forecasts.
8. Provide an interactive finance chatbot.
9. Demonstrate integration of Artificial Intelligence with a full-stack application.

---

## 🔮 Future Enhancements

Possible future improvements include:

* Bank account integrations
* Payment application integrations
* OCR-based receipt scanning
* Voice-based transaction entry
* Advanced AI chatbot
* Improved forecasting models
* Savings goals
* Anomaly detection
* Multilingual support
* Mobile application
* Cloud deployment
* Advanced authentication
* Personalized financial recommendations

---

## ⚠️ Limitations

* ML performance depends on the quality and quantity of training data.
* New users may have insufficient historical data for forecasting.
* Ambiguous transaction descriptions may result in incorrect categories.
* Spending forecasts are estimates and not guaranteed predictions.
* The chatbot provides basic financial information based on recorded data.
* This application is not a professional financial advisor.

---

## 👨‍💻 Project Information

**Project:** AI Finance Assistant

**Domain:** Artificial Intelligence & Machine Learning

**Technologies:** React, FastAPI, Python, SQLite, Scikit-learn

**Repository:**
https://github.com/nivas0998/AI-Finance-Assistant

---

## 📄 Disclaimer

This project is created for educational, internship, and portfolio purposes.

The information generated by this application should not be considered professional financial, investment, tax, banking, or legal advice.

Users should consult qualified professionals for real-world financial decisions.

---

## ⭐ Acknowledgement

This project demonstrates the practical integration of:

```text
Artificial Intelligence
        +
Machine Learning
        +
Backend APIs
        +
Database Management
        +
Frontend Development
        =
AI Finance Assistant
```

Built as an internship major project to demonstrate full-stack development and AI/ML application development.
