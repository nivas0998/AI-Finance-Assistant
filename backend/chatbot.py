
from backend.database import get_connection


def finance_chat(user_id, message):

    message = message.strip().lower()

    connection = get_connection()

    user = connection.execute(
        """
        SELECT name
        FROM users
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()

    if not user:
        connection.close()
        return "User not found."


    # --------------------------------------------------------
    # TOTAL INCOME
    # --------------------------------------------------------

    total_income = connection.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND type = 'income'
        """,
        (user_id,),
    ).fetchone()[0]


    # --------------------------------------------------------
    # TOTAL EXPENSE
    # --------------------------------------------------------

    total_expense = connection.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND type = 'expense'
        """,
        (user_id,),
    ).fetchone()[0]


    # --------------------------------------------------------
    # BALANCE
    # --------------------------------------------------------

    balance = total_income - total_expense


    # --------------------------------------------------------
    # HIGHEST SPENDING CATEGORY
    # --------------------------------------------------------

    highest_category = connection.execute(
        """
        SELECT
            COALESCE(category, 'Other') AS category,
            SUM(amount) AS total
        FROM transactions
        WHERE user_id = ?
        AND type = 'expense'
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
        """,
        (user_id,),
    ).fetchone()


    # --------------------------------------------------------
    # TRANSACTION COUNT
    # --------------------------------------------------------

    transaction_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()[0]


    connection.close()


    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    if any(
        word in message
        for word in [
            "hello",
            "hi",
            "hey",
            "hii",
            "hai",
        ]
    ):

        return (
            f"Hello {user['name']}! 👋 "
            "I'm your AI Finance Assistant. "
            "You can ask me about your income, "
            "expenses, balance, spending categories "
            "or transactions."
        )


    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    if (
        "help" in message
        or "what can you do" in message
        or "options" in message
    ):

        return (
            "I can help you with:\n\n"
            "• Total income\n"
            "• Total expenses\n"
            "• Current balance\n"
            "• Highest spending category\n"
            "• Number of transactions\n"
            "• Basic spending guidance"
        )


    # --------------------------------------------------------
    # INCOME
    # --------------------------------------------------------

    if (
        "income" in message
        or "earned" in message
        or "earning" in message
        or "salary" in message
    ):

        return (
            f"Your total recorded income is "
            f"₹{total_income:,.2f}."
        )


    # --------------------------------------------------------
    # EXPENSE
    # --------------------------------------------------------

    if (
        "expense" in message
        or "expenses" in message
        or "spent" in message
        or "spending" in message
    ):

        if "highest" in message or "category" in message:

            if highest_category:

                return (
                    f"Your highest recorded spending "
                    f"category is {highest_category['category']} "
                    f"with ₹{highest_category['total']:,.2f}."
                )

            return (
                "You don't have any recorded expenses yet."
            )

        return (
            f"Your total recorded expenses are "
            f"₹{total_expense:,.2f}."
        )


    # --------------------------------------------------------
    # BALANCE
    # --------------------------------------------------------

    if (
        "balance" in message
        or "remaining" in message
        or "left" in message
        or "money" in message
    ):

        return (
            f"Your current recorded balance is "
            f"₹{balance:,.2f}."
        )


    # --------------------------------------------------------
    # HIGHEST CATEGORY
    # --------------------------------------------------------

    if (
        "highest category" in message
        or "most spending" in message
        or "spend most" in message
        or "biggest expense" in message
        or "largest expense" in message
    ):

        if highest_category:

            return (
                f"{highest_category['category']} is your "
                f"highest spending category at "
                f"₹{highest_category['total']:,.2f}."
            )

        return (
            "There is not enough expense data "
            "to identify a highest spending category."
        )


    # --------------------------------------------------------
    # TRANSACTION COUNT
    # --------------------------------------------------------

    if (
        "transaction" in message
        or "transactions" in message
        or "records" in message
    ):

        return (
            f"You currently have "
            f"{transaction_count} recorded transactions."
        )


    # --------------------------------------------------------
    # SAVINGS
    # --------------------------------------------------------

    if (
        "save" in message
        or "saving" in message
        or "savings" in message
    ):

        if total_income <= 0:

            return (
                "Add some income records first so I can "
                "help you understand your recorded savings."
            )

        savings_rate = (
            balance / total_income
        ) * 100

        return (
            f"Your recorded balance is "
            f"₹{balance:,.2f}, which is approximately "
            f"{savings_rate:.1f}% of your recorded income."
        )


    # --------------------------------------------------------
    # ADVICE
    # --------------------------------------------------------

    if (
        "advice" in message
        or "suggestion" in message
        or "suggest" in message
        or "tip" in message
    ):

        if total_expense > total_income:

            return (
                "Your recorded expenses are higher than "
                "your recorded income. Consider reviewing "
                "your highest spending categories and "
                "existing budgets."
            )

        if total_income > 0 and balance > 0:

            return (
                "Your recorded income is currently higher "
                "than your recorded expenses. Continue "
                "tracking transactions and reviewing your "
                "budgets regularly."
            )

        return (
            "Keep recording your income and expenses "
            "regularly so that better spending insights "
            "can be generated."
        )


    # --------------------------------------------------------
    # DEFAULT RESPONSE
    # --------------------------------------------------------

    return (
        "I can answer questions about your recorded "
        "income, expenses, balance, spending categories "
        "and transactions.\n\n"
        "Try asking:\n"
        "• How much did I spend?\n"
        "• What is my balance?\n"
        "• What is my highest spending category?\n"
        "• How much income did I record?"
    )

