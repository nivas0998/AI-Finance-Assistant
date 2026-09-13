
import { Link } from "react-router-dom";
import {
  ArrowRight,
  Brain,
  ShieldCheck,
  BarChart3,
  Sparkles,
} from "lucide-react";

function Home() {
  return (
    <div className="home-page">

      {/* Navbar */}
      <nav className="home-navbar">
        <div className="brand">
          <div className="brand-mark">
            <Brain size={20} />
          </div>
          <span>AI Finance</span>
        </div>

        <div className="home-nav-links">
          <a href="#features">Features</a>
          <a href="#about">About</a>
        </div>

        <div className="home-nav-actions">
          <Link to="/login" className="nav-login">
            Login
          </Link>

          <Link to="/register" className="nav-register">
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <main className="home-hero">

        <div className="hero-content">

          <div className="hero-badge">
            <Sparkles size={14} />
            AI-powered personal finance
          </div>

          <h1>
            Your money.
            <br />
            <span>Understood.</span>
          </h1>

          <p>
            AI Finance Assistant helps you understand your spending,
            manage budgets, track transactions and discover meaningful
            financial patterns — all in one simple dashboard.
          </p>

          <div className="hero-actions">
            <Link to="/register" className="hero-primary">
              Start Managing
              <ArrowRight size={17} />
            </Link>

            <Link to="/login" className="hero-secondary">
              Sign In
            </Link>
          </div>

          <div className="hero-note">
            <ShieldCheck size={15} />
            Educational finance assistant · Your data stays yours
          </div>
        </div>

        {/* Dashboard visual */}
        <div className="hero-dashboard">

          <div className="dashboard-window">

            <div className="window-top">
              <div className="window-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>

              <span>AI Finance Assistant</span>
            </div>

            <div className="mini-dashboard">

              <div className="mini-header">
                <div>
                  <small>FINANCIAL OVERVIEW</small>
                  <h3>Dashboard</h3>
                </div>

                <div className="mini-status">
                  <span></span>
                  AI Active
                </div>
              </div>

              <div className="mini-cards">

                <div className="mini-card">
                  <small>Total Income</small>
                  <strong>₹25,000</strong>
                  <span className="positive">↑ Money received</span>
                </div>

                <div className="mini-card">
                  <small>Total Expenses</small>
                  <strong>₹8,450</strong>
                  <span className="negative">↓ Money spent</span>
                </div>

                <div className="mini-card">
                  <small>Balance</small>
                  <strong>₹16,550</strong>
                  <span className="positive">Healthy balance</span>
                </div>
              </div>

              <div className="mini-chart-card">

                <div className="mini-chart-header">
                  <div>
                    <small>MONTHLY ANALYSIS</small>
                    <strong>Spending Trend</strong>
                  </div>

                  <BarChart3 size={18} />
                </div>

                <div className="fake-chart">
                  <div className="chart-line line-one"></div>
                  <div className="chart-line line-two"></div>
                  <div className="chart-line line-three"></div>
                  <div className="chart-area"></div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </main>

      {/* Features */}
      <section id="features" className="home-features">

        <div className="section-heading">
          <span>CORE CAPABILITIES</span>
          <h2>Everything you need to understand your finances.</h2>
        </div>

        <div className="feature-grid">

          <div className="feature-card">
            <div className="feature-icon">
              <Brain size={22} />
            </div>

            <h3>AI Categorization</h3>

            <p>
              Automatically classify expenses into meaningful
              categories using machine learning.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <BarChart3 size={22} />
            </div>

            <h3>Smart Analytics</h3>

            <p>
              Understand category-wise spending and monthly
              financial trends through clear visualizations.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <ShieldCheck size={22} />
            </div>

            <h3>Budget Control</h3>

            <p>
              Set monthly budgets, monitor usage and receive
              alerts when spending approaches your limits.
            </p>
          </div>

        </div>
      </section>

      {/* About */}
      <section id="about" className="home-about">

        <div className="about-content">
          <span>BUILT FOR SIMPLICITY</span>

          <h2>
            Financial data should be
            <br />
            <strong>easy to understand.</strong>
          </h2>

          <p>
            AI Finance Assistant combines a clean financial dashboard
            with beginner-friendly machine learning to turn everyday
            transaction data into useful insights.
          </p>
        </div>

        <div className="about-card">
          <div className="about-card-icon">
            <Sparkles size={24} />
          </div>

          <h3>Learn from your spending</h3>

          <p>
            Discover where your money goes, compare spending against
            budgets and understand patterns in your financial activity.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="home-footer">
        <div className="brand">
          <div className="brand-mark">
            <Brain size={18} />
          </div>
          <span>AI Finance</span>
        </div>

        <p>
          © 2026 AI Finance Assistant. Educational portfolio project.
        </p>
      </footer>

    </div>
  );
}

export default Home;

