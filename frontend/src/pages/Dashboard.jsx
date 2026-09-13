
import { useEffect, useState } from "react";
import axios from "axios";
import {
  Brain,
  Wallet,
  TrendingUp,
  TrendingDown,
  Plus,
  Trash2,
  LogOut,
  RefreshCw,
  PieChart as PieChartIcon,
  Sparkles,
  Lightbulb,
  AlertTriangle,
  CheckCircle,
  Info,
  BarChart3,
  MessageCircle,
  Send,
  X,
} from "lucide-react";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

import { useNavigate } from "react-router-dom";


const API = "https://ai-finance-assistant-btxp.onrender.com";


const categories = [
  "Food",
  "Transport",
  "Shopping",
  "Bills",
  "Entertainment",
  "Health",
  "Education",
  "Other",
];


const chartColors = [
  "#4f7cff",
  "#8b5cf6",
  "#14b8a6",
  "#f59e0b",
  "#ef4444",
  "#06b6d4",
  "#22c55e",
  "#64748b",
];


function Dashboard() {

  const navigate = useNavigate();

  const userId = localStorage.getItem("user_id");
  const userName =
    localStorage.getItem("user_name") || "User";


  const [dashboard, setDashboard] =
    useState(null);

  const [transactions, setTransactions] =
    useState([]);

  const [budgets, setBudgets] =
    useState([]);

  const [insights, setInsights] =
    useState([]);

  const [forecast, setForecast] =
    useState(null);

  const [form, setForm] = useState({
    date: new Date()
      .toISOString()
      .split("T")[0],

    description: "",

    amount: "",

    type: "expense",

    category: "Food",
  });


  const [budgetForm, setBudgetForm] = useState({
    month: new Date()
      .toISOString()
      .slice(0, 7),

    category: "Food",

    limit_amount: "",
  });


  const [message, setMessage] =
    useState("");

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [predicting, setPredicting] =
    useState(false);

  const [prediction, setPrediction] =
    useState(null);

  const [insightsLoading, setInsightsLoading] =
    useState(false);

  const [forecastLoading, setForecastLoading] =
    useState(false);

  const [chatOpen, setChatOpen] =
    useState(false);

  const [chatInput, setChatInput] =
    useState("");

  const [chatLoading, setChatLoading] =
    useState(false);

  const [chatMessages, setChatMessages] =
    useState([
      {
        role: "bot",
        text: `Hello ${userName}! 👋 Ask me about your income, expenses, balance or spending categories.`,
      },
    ]);


  useEffect(() => {

    if (!userId) {
      navigate("/login");
      return;
    }

    loadData();

  }, []);


  const loadData = async () => {

    try {

      setLoading(true);
      setError("");

      const [
        dashboardResponse,
        transactionResponse,
        budgetResponse,
        insightsResponse,
        forecastResponse,
      ] = await Promise.all([

        axios.get(
          `${API}/dashboard/${userId}`
        ),

        axios.get(
          `${API}/transactions/${userId}`
        ),

        axios.get(
          `${API}/budgets/${userId}`
        ),

        axios.get(
          `${API}/insights/${userId}`
        ),

        axios.get(
          `${API}/forecast/${userId}`
        ),

      ]);


      setDashboard(
        dashboardResponse.data
      );

      setTransactions(
        transactionResponse.data
      );

      setBudgets(
        budgetResponse.data
      );

      setInsights(
        insightsResponse.data.insights
      );

      setForecast(
        forecastResponse.data
      );

    } catch (err) {

      console.error(err);

      setError(
        "Unable to load dashboard data."
      );

    } finally {

      setLoading(false);

    }
  };


  const handleChange = (event) => {

    const {
      name,
      value,
    } = event.target;


    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));


    setMessage("");
    setError("");


    if (name === "description") {
      setPrediction(null);
    }

  };


  const predictCategory = async () => {

    if (!form.description.trim()) {

      setError(
        "First enter a transaction description."
      );

      return;
    }


    try {

      setPredicting(true);

      setMessage("");
      setError("");
      setPrediction(null);


      const response = await axios.post(
        `${API}/predict-category`,
        {
          description:
            form.description,
        }
      );


      const predictedCategory =
        response.data.category;

      const confidence =
        response.data.confidence;


      setForm((previous) => ({
        ...previous,
        category:
          predictedCategory,
      }));


      setPrediction({
        category:
          predictedCategory,

        confidence:
          confidence,
      });


      setMessage(
        `AI predicted ${predictedCategory} with ${confidence}% confidence.`
      );

    } catch (err) {

      console.error(err);

      setError(
        err.response?.data?.detail ||
          "AI category prediction failed."
      );

    } finally {

      setPredicting(false);

    }

  };


  const addTransaction = async (
    event
  ) => {

    event.preventDefault();

    setMessage("");
    setError("");


    if (!form.description.trim()) {

      setError(
        "Please enter a transaction description."
      );

      return;
    }


    if (!form.amount) {

      setError(
        "Please enter an amount."
      );

      return;
    }


    try {

      await axios.post(
        `${API}/transactions`,
        {
          user_id:
            Number(userId),

          date:
            form.date,

          description:
            form.description,

          amount:
            Number(form.amount),

          type:
            form.type,

          category:
            form.category,
        }
      );


      setMessage(
        "Transaction added successfully."
      );


      setForm({
        date: new Date()
          .toISOString()
          .split("T")[0],

        description: "",

        amount: "",

        type: "expense",

        category: "Food",
      });


      setPrediction(null);


      await loadData();

    } catch (err) {

      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Failed to add transaction."
      );

    }

  };


  const deleteTransaction =
    async (transactionId) => {

      try {

        setError("");
        setMessage("");


        await axios.delete(
          `${API}/transactions/${transactionId}?user_id=${userId}`
        );


        setMessage(
          "Transaction deleted successfully."
        );


        await loadData();

      } catch (err) {

        console.error(err);

        setError(
          "Failed to delete transaction."
        );

      }

    };


  const createBudget = async (
    event
  ) => {

    event.preventDefault();

    setMessage("");
    setError("");


    if (!budgetForm.limit_amount) {

      setError(
        "Please enter budget amount."
      );

      return;
    }


    try {

      await axios.post(
        `${API}/budgets`,
        {
          user_id:
            Number(userId),

          month:
            budgetForm.month,

          category:
            budgetForm.category,

          limit_amount:
            Number(
              budgetForm.limit_amount
            ),
        }
      );


      setMessage(
        "Budget created successfully."
      );


      setBudgetForm({
        month: new Date()
          .toISOString()
          .slice(0, 7),

        category: "Food",

        limit_amount: "",
      });


      await loadData();

    } catch (err) {

      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Failed to create budget."
      );

    }

  };


  const refreshInsights =
    async () => {

      try {

        setInsightsLoading(true);


        const response =
          await axios.get(
            `${API}/insights/${userId}`
          );


        setInsights(
          response.data.insights
        );

      } catch (err) {

        console.error(err);

        setError(
          "Unable to refresh AI insights."
        );

      } finally {

        setInsightsLoading(false);

      }

    };


  const refreshForecast =
    async () => {

      try {

        setForecastLoading(true);

        setError("");


        const response =
          await axios.get(
            `${API}/forecast/${userId}`
          );


        setForecast(
          response.data
        );

      } catch (err) {

        console.error(err);

        setError(
          "Unable to generate spending forecast."
        );

      } finally {

        setForecastLoading(false);

      }

    };


  const sendChatMessage = async () => {
    const userMessage = chatInput.trim();

    if (!userMessage || chatLoading) {
      return;
    }

    setChatMessages((previous) => [
      ...previous,
      {
        role: "user",
        text: userMessage,
      },
    ]);

    setChatInput("");
    setChatLoading(true);

    try {
      const response = await axios.post(
        `${API}/chat`,
        {
          user_id: Number(userId),
          message: userMessage,
        }
      );

      setChatMessages((previous) => [
        ...previous,
        {
          role: "bot",
          text: response.data.response,
        },
      ]);
    } catch (err) {
      console.error(err);

      setChatMessages((previous) => [
        ...previous,
        {
          role: "bot",
          text: "Sorry, I couldn't process that request. Please try again.",
        },
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleChatKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendChatMessage();
    }
  };


  const logout = () => {

    localStorage.removeItem(
      "user_id"
    );

    localStorage.removeItem(
      "user_name"
    );

    navigate("/login");

  };


  if (!dashboard) {

    return (

      <div className="dashboard-loading">

        <Brain size={32} />

        <p>
          Loading your financial dashboard...
        </p>

      </div>

    );

  }


  const summary =
    dashboard.summary;


  const chartData =
    dashboard.category_spending
      .filter(
        (item) =>
          item.category
      )
      .map((item) => ({
        name:
          item.category,

        value:
          Number(item.total),
      }));


  const forecastChartData =
    forecast?.historical_data
      ? forecast.historical_data.map(
          (item) => ({
            month:
              item.month,

            spending:
              Number(item.expense),

            predicted:
              null,
          })
        )
      : [];


  if (
    forecast?.status ===
      "success" &&
    forecastChartData.length > 0
  ) {

    forecastChartData.push({
      month:
        forecast.next_month,

      spending:
        null,

      predicted:
        Number(
          forecast.predicted_spending
        ),
    });

  }


  const getInsightIcon =
    (type) => {

      if (type === "positive") {
        return <CheckCircle size={18} />;
      }

      if (
        type === "warning" ||
        type === "budget"
      ) {
        return (
          <AlertTriangle size={18} />
        );
      }

      if (type === "category") {
        return (
          <TrendingDown size={18} />
        );
      }

      if (type === "tip") {
        return (
          <Lightbulb size={18} />
        );
      }

      return <Info size={18} />;

    };


  return (

    <div className="dashboard-page">


      {/* NAVBAR */}

      <header className="dashboard-navbar">

        <div className="dashboard-brand">

          <div className="brand-mark">

            <Brain size={20} />

          </div>


          <div>

            <strong>
              AI Finance
            </strong>

            <span>
              Assistant
            </span>

          </div>

        </div>


        <div className="dashboard-user">

          <div className="user-info">

            <span>
              Welcome back
            </span>

            <strong>
              {userName}
            </strong>

          </div>


          <button
            className="logout-btn"
            onClick={logout}
          >

            <LogOut size={17} />

            Logout

          </button>

        </div>

      </header>


      <main className="dashboard-content">


        {/* PAGE HEADER */}

        <section className="dashboard-title">

          <div>

            <p className="dashboard-eyebrow">
              PERSONAL FINANCE
            </p>

            <h1>
              Your financial overview
            </h1>

            <p>
              Track your income, expenses
              and budgets from one place.
            </p>

          </div>


          <button
            className="refresh-btn"
            onClick={loadData}
          >

            <RefreshCw size={17} />

            {loading
              ? "Refreshing..."
              : "Refresh"}

          </button>

        </section>


        {/* MESSAGES */}

        {message && (

          <div className="dashboard-success">

            <Sparkles size={15} />

            <span>
              {message}
            </span>

          </div>

        )}


        {error && (

          <div className="dashboard-error">

            <span>
              {error}
            </span>

          </div>

        )}


        {/* SUMMARY */}

        <section className="summary-grid">


          <div className="summary-card">

            <div className="summary-icon income-icon">

              <TrendingUp size={22} />

            </div>


            <div>

              <span>
                Total Income
              </span>

              <h2>
                ₹
                {Number(
                  summary.total_income
                ).toLocaleString()}
              </h2>

            </div>

          </div>


          <div className="summary-card">

            <div className="summary-icon expense-icon">

              <TrendingDown size={22} />

            </div>


            <div>

              <span>
                Total Expenses
              </span>

              <h2>
                ₹
                {Number(
                  summary.total_expenses
                ).toLocaleString()}
              </h2>

            </div>

          </div>


          <div className="summary-card">

            <div className="summary-icon balance-icon">

              <Wallet size={22} />

            </div>


            <div>

              <span>
                Current Balance
              </span>

              <h2>
                ₹
                {Number(
                  summary.balance
                ).toLocaleString()}
              </h2>

            </div>

          </div>


        </section>


        {/* AI FINANCIAL INSIGHTS */}

        <section className="dashboard-panel ai-insights-panel">


          <div className="panel-heading">

            <div>

              <p className="panel-label">
                ARTIFICIAL INTELLIGENCE
              </p>

              <h2>

                <Sparkles size={19} />

                AI Financial Insights

              </h2>

            </div>


            <button
              className="insight-refresh-btn"
              onClick={refreshInsights}
              disabled={
                insightsLoading
              }
            >

              <RefreshCw
                size={15}
                className={
                  insightsLoading
                    ? "spin-icon"
                    : ""
                }
              />

              {insightsLoading
                ? "Analyzing..."
                : "Analyze"}

            </button>

          </div>


          <div className="insights-grid">

            {insights.map(
              (insight, index) => (

                <div
                  className={`insight-card insight-${insight.type}`}
                  key={`${insight.title}-${index}`}
                >

                  <div className="insight-icon">

                    {getInsightIcon(
                      insight.type
                    )}

                  </div>


                  <div>

                    <strong>
                      {insight.title}
                    </strong>

                    <p>
                      {insight.message}
                    </p>

                  </div>

                </div>

              )
            )}

          </div>


          <div className="ai-insights-footer">

            <Brain size={15} />

            <span>
              Insights are generated from
              your recorded financial activity
              and are for educational purposes
              only.
            </span>

          </div>

        </section>


        {/* AI SPENDING FORECAST */}

        <section className="dashboard-panel forecast-panel">


          <div className="panel-heading">

            <div>

              <p className="panel-label">
                MACHINE LEARNING
              </p>

              <h2>

                <BarChart3 size={19} />

                AI Spending Forecast

              </h2>

            </div>


            <button
              className="insight-refresh-btn"
              onClick={refreshForecast}
              disabled={
                forecastLoading
              }
            >

              <RefreshCw
                size={15}
                className={
                  forecastLoading
                    ? "spin-icon"
                    : ""
                }
              />

              {forecastLoading
                ? "Predicting..."
                : "Predict"}

            </button>

          </div>


          {forecast?.status ===
            "success" ? (

            <>

              <div className="forecast-summary">

                <div className="forecast-number-card">

                  <span>
                    PREDICTED NEXT MONTH
                  </span>

                  <strong>
                    ₹
                    {Number(
                      forecast.predicted_spending
                    ).toLocaleString()}
                  </strong>

                  <small>
                    {forecast.next_month}
                  </small>

                </div>


                <div className="forecast-model-card">

                  <div className="forecast-model-icon">

                    <Brain size={20} />

                  </div>


                  <div>

                    <span>
                      MODEL USED
                    </span>

                    <strong>
                      {forecast.model}
                    </strong>

                    <small>
                      R² Score:{" "}
                      {forecast.r2_score}
                    </small>

                  </div>

                </div>

              </div>


              <div className="forecast-chart">

                <ResponsiveContainer
                  width="100%"
                  height={250}
                >

                  <BarChart
                    data={
                      forecastChartData
                    }
                  >

                    <CartesianGrid
                      strokeDasharray="3 3"
                      stroke="rgba(255,255,255,0.06)"
                    />

                    <XAxis
                      dataKey="month"
                      stroke="#68748a"
                      fontSize={10}
                    />

                    <YAxis
                      stroke="#68748a"
                      fontSize={10}
                    />

                    <Tooltip
                      formatter={(
                        value,
                        name
                      ) => {

                        if (
                          value === null ||
                          value === undefined
                        ) {
                          return [
                            "-",
                            name,
                          ];
                        }

                        return [
                          `₹${Number(
                            value
                          ).toLocaleString()}`,
                          name,
                        ];

                      }}
                    />


                    <Bar
                      dataKey="spending"
                      name="Historical Spending"
                      fill="#4f7cff"
                      radius={[
                        5,
                        5,
                        0,
                        0,
                      ]}
                    />


                    <Bar
                      dataKey="predicted"
                      name="Predicted Spending"
                      fill="#8b5cf6"
                      radius={[
                        5,
                        5,
                        0,
                        0,
                      ]}
                    />

                  </BarChart>

                </ResponsiveContainer>

              </div>


              <div className="forecast-note">

                <Brain size={15} />

                <span>
                  This forecast is an estimate
                  based on your historical spending
                  and should not be treated as a
                  guaranteed future result.
                </span>

              </div>

            </>

          ) : (

            <div className="forecast-empty">

              <div className="forecast-empty-icon">

                <BarChart3 size={30} />

              </div>


              <h3>
                Not enough historical data
              </h3>


              <p>
                {forecast?.message ||
                  "Add expenses from at least two different months to generate a spending forecast."}
              </p>


              <button
                className="insight-refresh-btn"
                onClick={refreshForecast}
              >

                <RefreshCw size={15} />

                Check Forecast

              </button>

            </div>

          )}

        </section>


        {/* TRANSACTION + SPENDING CHART */}

        <section className="dashboard-main-grid">


          {/* ADD TRANSACTION */}

          <div className="dashboard-panel">

            <div className="panel-heading">

              <div>

                <p className="panel-label">
                  TRANSACTIONS
                </p>

                <h2>
                  Add transaction
                </h2>

              </div>


              <div className="panel-heading-icon">

                <Plus size={19} />

              </div>

            </div>


            <form
              className="transaction-form"
              onSubmit={
                addTransaction
              }
            >


              <div className="form-row">


                <div className="dashboard-field">

                  <label>
                    Date
                  </label>

                  <input
                    type="date"
                    name="date"
                    value={
                      form.date
                    }
                    onChange={
                      handleChange
                    }
                  />

                </div>


                <div className="dashboard-field">

                  <label>
                    Type
                  </label>

                  <select
                    name="type"
                    value={
                      form.type
                    }
                    onChange={
                      handleChange
                    }
                  >

                    <option value="expense">
                      Expense
                    </option>

                    <option value="income">
                      Income
                    </option>

                  </select>

                </div>

              </div>


              <div className="dashboard-field">

                <label>
                  Description
                </label>

                <input
                  type="text"
                  name="description"
                  placeholder="e.g. Lunch at restaurant"
                  value={
                    form.description
                  }
                  onChange={
                    handleChange
                  }
                />

              </div>


              <div className="form-row">


                <div className="dashboard-field">

                  <label>
                    Amount
                  </label>

                  <input
                    type="number"
                    name="amount"
                    min="1"
                    placeholder="₹ 0"
                    value={
                      form.amount
                    }
                    onChange={
                      handleChange
                    }
                  />

                </div>


                <div className="dashboard-field">

                  <label>
                    Category
                  </label>

                  <select
                    name="category"
                    value={
                      form.category
                    }
                    onChange={
                      handleChange
                    }
                  >

                    {categories.map(
                      (category) => (

                        <option
                          key={category}
                          value={
                            category
                          }
                        >
                          {category}
                        </option>

                      )
                    )}

                  </select>


                  <button
                    type="button"
                    className="ai-predict-btn"
                    onClick={
                      predictCategory
                    }
                    disabled={
                      predicting
                    }
                  >

                    <Brain size={15} />

                    {predicting
                      ? "AI is analyzing..."
                      : "✨ AI Predict Category"}

                  </button>

                </div>

              </div>


              {prediction && (

                <div className="ai-result-box">

                  <div className="ai-result-icon">

                    <Brain size={18} />

                  </div>


                  <div>

                    <span>
                      AI Prediction
                    </span>

                    <strong>
                      {
                        prediction.category
                      }
                    </strong>

                    <small>
                      Confidence:{" "}
                      {
                        prediction.confidence
                      }%
                    </small>

                  </div>

                </div>

              )}


              <button
                className="primary-dashboard-btn"
                type="submit"
              >

                <Plus size={17} />

                Add Transaction

              </button>

            </form>

          </div>


          {/* PIE CHART */}

          <div className="dashboard-panel">

            <div className="panel-heading">

              <div>

                <p className="panel-label">
                  ANALYTICS
                </p>

                <h2>
                  Spending by category
                </h2>

              </div>


              <PieChartIcon size={20} />

            </div>


            {chartData.length > 0 ? (

              <div className="chart-wrapper">

                <ResponsiveContainer
                  width="100%"
                  height={240}
                >

                  <PieChart>

                    <Pie
                      data={chartData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      outerRadius={85}
                      innerRadius={48}
                      paddingAngle={3}
                    >

                      {chartData.map(
                        (
                          entry,
                          index
                        ) => (

                          <Cell
                            key={
                              `cell-${index}`
                            }
                            fill={
                              chartColors[
                                index %
                                  chartColors.length
                              ]
                            }
                          />

                        )
                      )}

                    </Pie>


                    <Tooltip
                      formatter={
                        (value) =>
                          `₹${Number(
                            value
                          ).toLocaleString()}`
                      }
                    />

                  </PieChart>

                </ResponsiveContainer>


                <div className="chart-legend">

                  {chartData.map(
                    (
                      item,
                      index
                    ) => (

                      <div
                        className="legend-item"
                        key={
                          item.name
                        }
                      >

                        <span
                          className="legend-dot"
                          style={{
                            background:
                              chartColors[
                                index %
                                  chartColors.length
                              ],
                          }}
                        />

                        <span>
                          {item.name}
                        </span>

                        <strong>
                          ₹
                          {Number(
                            item.value
                          ).toLocaleString()}
                        </strong>

                      </div>

                    )
                  )}

                </div>

              </div>

            ) : (

              <div className="empty-chart">

                <PieChartIcon size={40} />

                <p>
                  No expense data yet.
                </p>

                <span>
                  Add an expense to see
                  analytics.
                </span>

              </div>

            )}

          </div>

        </section>


        {/* TRANSACTION HISTORY */}

        <section className="dashboard-panel transaction-panel">


          <div className="panel-heading">

            <div>

              <p className="panel-label">
                HISTORY
              </p>

              <h2>
                Recent transactions
              </h2>

            </div>


            <span className="transaction-count">

              {transactions.length}
              {" "}
              records

            </span>

          </div>


          {transactions.length > 0 ? (

            <div className="transaction-table-wrapper">

              <table className="transaction-table">

                <thead>

                  <tr>

                    <th>
                      Date
                    </th>

                    <th>
                      Description
                    </th>

                    <th>
                      Category
                    </th>

                    <th>
                      Type
                    </th>

                    <th>
                      Amount
                    </th>

                    <th></th>

                  </tr>

                </thead>


                <tbody>

                  {transactions.map(
                    (transaction) => (

                      <tr
                        key={
                          transaction.transaction_id
                        }
                      >

                        <td>
                          {
                            transaction.date
                          }
                        </td>


                        <td className="transaction-description">

                          {
                            transaction.description
                          }

                        </td>


                        <td>

                          <span className="category-badge">

                            {
                              transaction.category ||
                              "Other"
                            }

                          </span>

                        </td>


                        <td>

                          <span
                            className={
                              transaction.type ===
                              "income"
                                ? "type-badge income-badge"
                                : "type-badge expense-badge"
                            }
                          >

                            {
                              transaction.type
                            }

                          </span>

                        </td>


                        <td
                          className={
                            transaction.type ===
                            "income"
                              ? "amount-income"
                              : "amount-expense"
                          }
                        >

                          {
                            transaction.type ===
                            "income"
                              ? "+"
                              : "-"
                          }

                          ₹
                          {Number(
                            transaction.amount
                          ).toLocaleString()}

                        </td>


                        <td>

                          <button
                            className="delete-btn"
                            onClick={() =>
                              deleteTransaction(
                                transaction.transaction_id
                              )
                            }
                          >

                            <Trash2 size={16} />

                          </button>

                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>

          ) : (

            <div className="empty-transactions">

              <Wallet size={35} />

              <p>
                No transactions yet.
              </p>

              <span>
                Add your first income or
                expense above.
              </span>

            </div>

          )}

        </section>


        {/* BUDGET SECTION */}

        <section className="dashboard-main-grid">


          {/* CREATE BUDGET */}

          <div className="dashboard-panel">

            <div className="panel-heading">

              <div>

                <p className="panel-label">
                  BUDGET
                </p>

                <h2>
                  Create monthly budget
                </h2>

              </div>

            </div>


            <form
              className="transaction-form"
              onSubmit={
                createBudget
              }
            >


              <div className="form-row">


                <div className="dashboard-field">

                  <label>
                    Month
                  </label>

                  <input
                    type="month"
                    value={
                      budgetForm.month
                    }
                    onChange={
                      (event) =>
                        setBudgetForm({
                          ...budgetForm,
                          month:
                            event.target.value,
                        })
                    }
                  />

                </div>


                <div className="dashboard-field">

                  <label>
                    Category
                  </label>

                  <select
                    value={
                      budgetForm.category
                    }
                    onChange={
                      (event) =>
                        setBudgetForm({
                          ...budgetForm,
                          category:
                            event.target.value,
                        })
                    }
                  >

                    {categories.map(
                      (category) => (

                        <option
                          key={
                            category
                          }
                          value={
                            category
                          }
                        >
                          {category}
                        </option>

                      )
                    )}

                  </select>

                </div>

              </div>


              <div className="dashboard-field">

                <label>
                  Budget Limit
                </label>

                <input
                  type="number"
                  min="1"
                  placeholder="₹ 0"
                  value={
                    budgetForm.limit_amount
                  }
                  onChange={
                    (event) =>
                      setBudgetForm({
                        ...budgetForm,
                        limit_amount:
                          event.target.value,
                      })
                  }
                />

              </div>


              <button
                className="primary-dashboard-btn"
                type="submit"
              >

                Create Budget

              </button>

            </form>

          </div>


          {/* BUDGET OVERVIEW */}

          <div className="dashboard-panel">

            <div className="panel-heading">

              <div>

                <p className="panel-label">
                  YOUR LIMITS
                </p>

                <h2>
                  Budget overview
                </h2>

              </div>

            </div>


            {budgets.length > 0 ? (

              <div className="budget-list">

                {budgets.map(
                  (budget) => (

                    <div
                      className="budget-item"
                      key={
                        budget.budget_id
                      }
                    >

                      <div className="budget-top">

                        <div>

                          <strong>
                            {
                              budget.category
                            }
                          </strong>

                          <span>
                            {
                              budget.month
                            }
                          </span>

                        </div>


                        <strong>
                          ₹
                          {Number(
                            budget.limit_amount
                          ).toLocaleString()}
                        </strong>

                      </div>


                      <div className="budget-progress">

                        <div
                          style={{
                            width: "0%",
                          }}
                        />

                      </div>


                      <p>
                        Monthly budget limit
                      </p>

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="empty-chart">

                <Wallet size={38} />

                <p>
                  No budgets created.
                </p>

                <span>
                  Create a category budget
                  to track spending.
                </span>

              </div>

            )}

          </div>

        </section>


        {/* DISCLAIMER */}

        <div className="dashboard-disclaimer">

          <Brain size={16} />

          <span>
            AI Finance Assistant is an
            educational project and does not
            provide professional financial,
            tax, or investment advice.
          </span>

        </div>


      </main>

      <button
        className="chatbot-floating-btn"
        onClick={() => setChatOpen((previous) => !previous)}
        aria-label="Open finance chatbot"
      >
        {chatOpen ? <X size={22} /> : <MessageCircle size={22} />}
      </button>

      {chatOpen && (
        <div className="chatbot-window">

          <div className="chatbot-header">

            <div className="chatbot-header-info">

              <div className="chatbot-avatar">
                <Brain size={19} />
              </div>

              <div>
                <strong>Finance Assistant</strong>
                <span>AI financial chatbot</span>
              </div>

            </div>

            <button
              className="chatbot-close-btn"
              onClick={() => setChatOpen(false)}
              aria-label="Close chatbot"
            >
              <X size={17} />
            </button>

          </div>


          <div className="chatbot-messages">

            {chatMessages.map((chat, index) => (
              <div
                key={`${chat.role}-${index}`}
                className={`chatbot-message-row ${chat.role}`}
              >

                {chat.role === "bot" && (
                  <div className="chatbot-small-avatar">
                    <Brain size={13} />
                  </div>
                )}

                <div className="chatbot-message">
                  {chat.text}
                </div>

              </div>
            ))}


            {chatLoading && (
              <div className="chatbot-message-row bot">

                <div className="chatbot-small-avatar">
                  <Brain size={13} />
                </div>

                <div className="chatbot-message chatbot-typing">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

              </div>
            )}

          </div>


          <div className="chatbot-suggestions">

            <button
              onClick={() =>
                setChatInput("How much did I spend?")
              }
            >
              Total expenses
            </button>

            <button
              onClick={() =>
                setChatInput("What is my balance?")
              }
            >
              My balance
            </button>

            <button
              onClick={() =>
                setChatInput(
                  "What is my highest spending category?"
                )
              }
            >
              Highest category
            </button>

          </div>


          <div className="chatbot-input-area">

            <textarea
              value={chatInput}
              onChange={(event) =>
                setChatInput(event.target.value)
              }
              onKeyDown={handleChatKeyDown}
              placeholder="Ask about your finances..."
              rows={1}
            />

            <button
              className="chatbot-send-btn"
              onClick={sendChatMessage}
              disabled={!chatInput.trim() || chatLoading}
              aria-label="Send message"
            >
              <Send size={17} />
            </button>

          </div>


          <div className="chatbot-disclaimer">
            <Brain size={12} />
            <span>Educational financial assistant</span>
          </div>

        </div>
      )}


    </div>

  );

}


export default Dashboard;

