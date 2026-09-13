from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import bcrypt

from backend.database import create_database, get_connection
from backend.schemas import (
    UserCreate,
    UserLogin,
    TransactionCreate,
    BudgetCreate,
)

from ml.predict import predict_category
from ml.forecast import forecast_spending
from backend.chatbot import finance_chat


app = FastAPI(title="AI Finance Assistant API")


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ai-finance-assistant-chi.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATABASE STARTUP
# ============================================================

@app.on_event("startup")
def startup():
    create_database()


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "AI Finance Assistant API is running"
    }


# ============================================================
# AUTHENTICATION
# ============================================================

@app.post("/register")
def register(user: UserCreate):

    connection = get_connection()

    existing_user = connection.execute(
        "SELECT user_id FROM users WHERE email = ?",
        (user.email,),
    ).fetchone()

    if existing_user:
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    password_hash = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")

    cursor = connection.execute(
        """
        INSERT INTO users
        (
            name,
            email,
            password_hash
        )
        VALUES (?, ?, ?)
        """,
        (
            user.name,
            user.email,
            password_hash,
        ),
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Registration successful",
        "user_id": user_id,
        "name": user.name,
    }


@app.post("/login")
def login(user: UserLogin):

    connection = get_connection()

    database_user = connection.execute(
        """
        SELECT
            user_id,
            name,
            email,
            password_hash
        FROM users
        WHERE email = ?
        """,
        (user.email,),
    ).fetchone()

    connection.close()

    if not database_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    password_valid = bcrypt.checkpw(
        user.password.encode("utf-8"),
        database_user["password_hash"].encode("utf-8"),
    )

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return {
        "message": "Login successful",
        "user_id": database_user["user_id"],
        "name": database_user["name"],
    }


# ============================================================
# AI EXPENSE CATEGORY PREDICTION
# ============================================================

@app.post("/predict-category")
def predict_expense_category(data: dict):

    description = data.get("description")

    if not description:
        raise HTTPException(
            status_code=400,
            detail="Description is required",
        )

    try:

        result = predict_category(description)

        return {
            "description": description,
            "category": result["category"],
            "confidence": result["confidence"],
        }

    except Exception as error:

        print("Prediction error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to predict expense category",
        )


# ============================================================
# AI FINANCIAL INSIGHTS
# ============================================================

@app.get("/insights/{user_id}")
def get_insights(user_id: int):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT
            user_id,
            name
        FROM users
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()

    if not user:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    total_income = connection.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND type = 'income'
        """,
        (user_id,),
    ).fetchone()[0]

    total_expenses = connection.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND type = 'expense'
        """,
        (user_id,),
    ).fetchone()[0]

    category_rows = connection.execute(
        """
        SELECT
            COALESCE(category, 'Other') AS category,
            SUM(amount) AS total
        FROM transactions
        WHERE user_id = ?
        AND type = 'expense'
        GROUP BY category
        ORDER BY total DESC
        """,
        (user_id,),
    ).fetchall()

    budget_rows = connection.execute(
        """
        SELECT
            budget_id,
            month,
            category,
            limit_amount
        FROM budgets
        WHERE user_id = ?
        ORDER BY month DESC
        """,
        (user_id,),
    ).fetchall()

    connection.close()

    balance = total_income - total_expenses

    insights = []

    if total_income == 0 and total_expenses == 0:

        insights.append(
            {
                "type": "info",
                "title": "Start tracking",
                "message": (
                    "Add your income and expenses to receive "
                    "personalized financial insights."
                ),
            }
        )

    else:

        if total_expenses > total_income:

            insights.append(
                {
                    "type": "warning",
                    "title": "Expenses are higher than income",
                    "message": (
                        "Your recorded expenses are currently "
                        "higher than your recorded income. "
                        "Review your spending categories."
                    ),
                }
            )

        elif total_income > 0:

            savings_rate = (
                balance / total_income
            ) * 100

            if savings_rate >= 30:

                insights.append(
                    {
                        "type": "positive",
                        "title": "Healthy balance",
                        "message": (
                            f"Your current recorded balance is "
                            f"₹{balance:,.2f}. Your recorded "
                            f"savings rate is approximately "
                            f"{savings_rate:.1f}%."
                        ),
                    }
                )

            elif savings_rate >= 10:

                insights.append(
                    {
                        "type": "info",
                        "title": "Room to improve",
                        "message": (
                            f"You currently retain approximately "
                            f"{savings_rate:.1f}% of your recorded "
                            "income. Reviewing discretionary "
                            "expenses may help."
                        ),
                    }
                )

            else:

                insights.append(
                    {
                        "type": "warning",
                        "title": "Low remaining balance",
                        "message": (
                            "Most of your recorded income is "
                            "currently being used by expenses. "
                            "Consider reviewing high-spending areas."
                        ),
                    }
                )

    if category_rows:

        highest_category = category_rows[0]["category"]
        highest_amount = category_rows[0]["total"]

        insights.append(
            {
                "type": "category",
                "title": "Highest spending category",
                "message": (
                    f"{highest_category} is your highest recorded "
                    f"expense category at ₹{highest_amount:,.2f}."
                ),
            }
        )

        if total_expenses > 0:

            percentage = (
                highest_amount / total_expenses
            ) * 100

            if percentage >= 40:

                insights.append(
                    {
                        "type": "warning",
                        "title": "Concentrated spending",
                        "message": (
                            f"{highest_category} represents "
                            f"approximately {percentage:.1f}% of "
                            "your recorded expenses."
                        ),
                    }
                )

    if budget_rows:

        for budget in budget_rows:

            connection = get_connection()

            spent = connection.execute(
                """
                SELECT COALESCE(SUM(amount), 0)
                FROM transactions
                WHERE user_id = ?
                AND type = 'expense'
                AND category = ?
                AND strftime('%Y-%m', date) = ?
                """,
                (
                    user_id,
                    budget["category"],
                    budget["month"],
                ),
            ).fetchone()[0]

            connection.close()

            limit_amount = budget["limit_amount"]

            if limit_amount > 0:

                percentage = (
                    spent / limit_amount
                ) * 100

                if percentage > 100:

                    insights.append(
                        {
                            "type": "budget",
                            "title": "Budget exceeded",
                            "message": (
                                f"{budget['category']} budget for "
                                f"{budget['month']} has been exceeded "
                                f"by ₹{spent - limit_amount:,.2f}."
                            ),
                        }
                    )

                elif percentage >= 80:

                    insights.append(
                        {
                            "type": "budget",
                            "title": "Budget almost reached",
                            "message": (
                                f"{budget['category']} spending has "
                                f"reached {percentage:.1f}% of the "
                                "current budget limit."
                            ),
                        }
                    )

                break

    if len(insights) < 3:

        insights.append(
            {
                "type": "tip",
                "title": "Track consistently",
                "message": (
                    "Continue recording transactions regularly "
                    "to make your spending analysis more useful."
                ),
            }
        )

    return {
        "user_id": user_id,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "insights": insights[:5],
    }


# ============================================================
# SPENDING FORECAST
# ============================================================

@app.get("/forecast/{user_id}")
def get_spending_forecast(user_id: int):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT user_id
        FROM users
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()

    connection.close()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    try:

        result = forecast_spending(user_id)

        return result

    except Exception as error:

        print("Forecast error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate spending forecast",
        )


# ============================================================
# FINANCE CHATBOT
# ============================================================

@app.post("/chat")
def chat(data: dict):

    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id:

        raise HTTPException(
            status_code=400,
            detail="User ID is required",
        )

    if not message or not str(message).strip():

        raise HTTPException(
            status_code=400,
            detail="Message is required",
        )

    try:

        response = finance_chat(
            int(user_id),
            str(message),
        )

        return {
            "message": message,
            "response": response,
        }

    except Exception as error:

        print("Chatbot error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to process chatbot request",
        )


# ============================================================
# TRANSACTIONS
# ============================================================

@app.post("/transactions")
def add_transaction(transaction: TransactionCreate):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT user_id
        FROM users
        WHERE user_id = ?
        """,
        (transaction.user_id,),
    ).fetchone()

    if not user:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if transaction.amount <= 0:

        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero",
        )

    if transaction.type not in [
        "income",
        "expense",
    ]:

        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Type must be income or expense",
        )

    cursor = connection.execute(
        """
        INSERT INTO transactions
        (
            user_id,
            date,
            description,
            amount,
            type,
            category
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            transaction.user_id,
            str(transaction.date),
            transaction.description,
            transaction.amount,
            transaction.type,
            transaction.category,
        ),
    )

    connection.commit()

    transaction_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Transaction added successfully",
        "transaction_id": transaction_id,
    }


@app.get("/transactions/{user_id}")
def get_transactions(user_id: int):

    connection = get_connection()

    transactions = connection.execute(
        """
        SELECT
            transaction_id,
            user_id,
            date,
            description,
            amount,
            type,
            category
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC, transaction_id DESC
        """,
        (user_id,),
    ).fetchall()

    connection.close()

    return [
        dict(transaction)
        for transaction in transactions
    ]


@app.put("/transactions/{transaction_id}")
def update_transaction(
    transaction_id: int,
    transaction: TransactionCreate,
):

    connection = get_connection()

    existing_transaction = connection.execute(
        """
        SELECT transaction_id
        FROM transactions
        WHERE transaction_id = ?
        AND user_id = ?
        """,
        (
            transaction_id,
            transaction.user_id,
        ),
    ).fetchone()

    if not existing_transaction:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    if transaction.amount <= 0:

        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero",
        )

    if transaction.type not in [
        "income",
        "expense",
    ]:

        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Type must be income or expense",
        )

    connection.execute(
        """
        UPDATE transactions
        SET
            date = ?,
            description = ?,
            amount = ?,
            type = ?,
            category = ?
        WHERE transaction_id = ?
        AND user_id = ?
        """,
        (
            str(transaction.date),
            transaction.description,
            transaction.amount,
            transaction.type,
            transaction.category,
            transaction_id,
            transaction.user_id,
        ),
    )

    connection.commit()
    connection.close()

    return {
        "message": "Transaction updated successfully",
    }


@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    user_id: int,
):

    connection = get_connection()

    existing_transaction = connection.execute(
        """
        SELECT transaction_id
        FROM transactions
        WHERE transaction_id = ?
        AND user_id = ?
        """,
        (
            transaction_id,
            user_id,
        ),
    ).fetchone()

    if not existing_transaction:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    connection.execute(
        """
        DELETE FROM transactions
        WHERE transaction_id = ?
        AND user_id = ?
        """,
        (
            transaction_id,
            user_id,
        ),
    )

    connection.commit()
    connection.close()

    return {
        "message": "Transaction deleted successfully",
    }


# ============================================================
# BUDGETS
# ============================================================

@app.post("/budgets")
def create_budget(budget: BudgetCreate):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT user_id
        FROM users
        WHERE user_id = ?
        """,
        (budget.user_id,),
    ).fetchone()

    if not user:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if budget.limit_amount <= 0:

        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Budget amount must be greater than zero",
        )

    cursor = connection.execute(
        """
        INSERT INTO budgets
        (
            user_id,
            month,
            category,
            limit_amount
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            budget.user_id,
            budget.month,
            budget.category,
            budget.limit_amount,
        ),
    )

    connection.commit()

    budget_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Budget created successfully",
        "budget_id": budget_id,
    }


@app.get("/budgets/{user_id}")
def get_budgets(user_id: int):

    connection = get_connection()

    budgets = connection.execute(
        """
        SELECT
            budget_id,
            user_id,
            month,
            category,
            limit_amount
        FROM budgets
        WHERE user_id = ?
        ORDER BY month DESC
        """,
        (user_id,),
    ).fetchall()

    connection.close()

    return [
        dict(budget)
        for budget in budgets
    ]


@app.get("/budgets/{user_id}/status")
def budget_status(user_id: int):

    connection = get_connection()

    budgets = connection.execute(
        """
        SELECT
            budget_id,
            month,
            category,
            limit_amount
        FROM budgets
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchall()

    result = []

    for budget in budgets:

        spent = connection.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE user_id = ?
            AND type = 'expense'
            AND category = ?
            AND strftime('%Y-%m', date) = ?
            """,
            (
                user_id,
                budget["category"],
                budget["month"],
            ),
        ).fetchone()[0]

        percentage = (
            spent / budget["limit_amount"]
        ) * 100 if budget["limit_amount"] > 0 else 0

        if spent > budget["limit_amount"]:

            status = "Budget exceeded"

        elif percentage >= 80:

            status = "Budget almost reached"

        else:

            status = "Within budget"

        result.append(
            {
                "budget_id": budget["budget_id"],
                "month": budget["month"],
                "category": budget["category"],
                "limit_amount": budget["limit_amount"],
                "spent": spent,
                "percentage": round(
                    percentage,
                    2,
                ),
                "status": status,
            }
        )

    connection.close()

    return result


# ============================================================
# DASHBOARD
# ============================================================

@app.get("/dashboard/{user_id}")
def dashboard(user_id: int):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT user_id
        FROM users
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()

    if not user:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    total_income = connection.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND type = 'income'
        """,
        (user_id,),
    ).fetchone()[0]

    total_expenses = connection.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND type = 'expense'
        """,
        (user_id,),
    ).fetchone()[0]

    category_spending = connection.execute(
        """
        SELECT
            category,
            SUM(amount) AS total
        FROM transactions
        WHERE user_id = ?
        AND type = 'expense'
        GROUP BY category
        ORDER BY total DESC
        """,
        (user_id,),
    ).fetchall()

    monthly_trends = connection.execute(
        """
        SELECT
            strftime('%Y-%m', date) AS month,

            SUM(
                CASE
                    WHEN type = 'income'
                    THEN amount
                    ELSE 0
                END
            ) AS income,

            SUM(
                CASE
                    WHEN type = 'expense'
                    THEN amount
                    ELSE 0
                END
            ) AS expenses

        FROM transactions

        WHERE user_id = ?

        GROUP BY strftime('%Y-%m', date)

        ORDER BY month
        """,
        (user_id,),
    ).fetchall()

    connection.close()

    balance = (
        total_income -
        total_expenses
    )

    return {
        "user_id": user_id,

        "summary": {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
        },

        "category_spending": [
            dict(item)
            for item in category_spending
        ],

        "monthly_trends": [
            dict(item)
            for item in monthly_trends
        ],
    }