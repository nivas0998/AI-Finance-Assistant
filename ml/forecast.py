
import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression


DATABASE_NAME = "finance.db"


def forecast_spending(user_id):
    connection = sqlite3.connect(DATABASE_NAME)

    rows = connection.execute(
        """
        SELECT
            strftime('%Y-%m', date) AS month,
            SUM(amount) AS total_expense
        FROM transactions
        WHERE user_id = ?
        AND type = 'expense'
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month
        """,
        (user_id,),
    ).fetchall()

    connection.close()

    # Need at least 2 months of historical data
    if len(rows) < 2:
        return {
            "status": "insufficient_data",
            "message": (
                "Not enough historical data. "
                "Add expenses from at least two different months "
                "to generate a spending forecast."
            ),
            "historical_data": [
                {
                    "month": row[0],
                    "expense": round(float(row[1]), 2),
                }
                for row in rows
            ],
            "predicted_spending": None,
            "next_month": None,
        }

    months = [row[0] for row in rows]
    expenses = [float(row[1]) for row in rows]

    # Convert months into numerical sequence
    X = np.array(
        range(1, len(expenses) + 1)
    ).reshape(-1, 1)

    y = np.array(expenses)

    # Linear Regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next month
    next_month_number = len(expenses) + 1

    predicted_amount = model.predict(
        np.array([[next_month_number]])
    )[0]

    # Spending cannot be negative
    predicted_amount = max(
        0,
        float(predicted_amount)
    )

    # Calculate model R² score
    r2_score = model.score(X, y)

    # Calculate next month label
    last_year, last_month = map(
        int,
        months[-1].split("-")
    )

    if last_month == 12:
        next_year = last_year + 1
        next_month = 1
    else:
        next_year = last_year
        next_month = last_month + 1

    next_month_label = (
        f"{next_year}-{next_month:02d}"
    )

    return {
        "status": "success",
        "message": (
            "Spending forecast generated successfully."
        ),
        "historical_data": [
            {
                "month": row[0],
                "expense": round(float(row[1]), 2),
            }
            for row in rows
        ],
        "predicted_spending": round(
            predicted_amount,
            2
        ),
        "next_month": next_month_label,
        "model": "Linear Regression",
        "r2_score": round(
            float(r2_score),
            3
        ),
    }

