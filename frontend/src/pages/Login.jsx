
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import {
  Brain,
  Mail,
  Lock,
  ArrowRight,
  ShieldCheck,
  AlertCircle,
} from "lucide-react";

function Login() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    if (error) {
      setError("");
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    if (!formData.email || !formData.password) {
      setError("Please enter your email and password.");
      return;
    }

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/login",
        {
          email: formData.email,
          password: formData.password,
        }
      );

      localStorage.setItem(
        "user_id",
        String(response.data.user_id)
      );

      localStorage.setItem(
        "user_name",
        response.data.name
      );

      navigate("/dashboard");
    } catch (err) {
      console.error(err);

      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError(
          "Unable to connect to the server. Please try again."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">

      {/* Background */}
      <div className="auth-background"></div>

      {/* Logo */}
      <Link to="/" className="auth-brand">
        <div className="brand-mark">
          <Brain size={20} />
        </div>

        <span>AI Finance</span>
      </Link>

      {/* Login Card */}
      <div className="auth-container">

        <div className="auth-card">

          <div className="auth-heading">
            <div className="auth-icon">
              <Brain size={24} />
            </div>

            <p className="auth-eyebrow">
              AI FINANCE ASSISTANT
            </p>

            <h1>Welcome back.</h1>

            <p>
              Sign in to continue managing your finances.
            </p>
          </div>

          {/* Error */}
          {error && (
            <div className="auth-error">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          <form
            className="auth-form"
            onSubmit={handleSubmit}
          >

            {/* Email */}
            <div className="auth-field">
              <label htmlFor="email">
                Email address
              </label>

              <div className="auth-input-wrapper">
                <Mail size={17} />

                <input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="you@example.com"
                  value={formData.email}
                  onChange={handleChange}
                  autoComplete="email"
                />
              </div>
            </div>

            {/* Password */}
            <div className="auth-field">
              <label htmlFor="password">
                Password
              </label>

              <div className="auth-input-wrapper">
                <Lock size={17} />

                <input
                  id="password"
                  name="password"
                  type="password"
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleChange}
                  autoComplete="current-password"
                />
              </div>
            </div>

            {/* Login */}
            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="auth-spinner"></span>
                  Signing in...
                </>
              ) : (
                <>
                  Sign in
                  <ArrowRight size={17} />
                </>
              )}
            </button>
          </form>

          {/* Security */}
          <div className="auth-security">
            <ShieldCheck size={15} />

            <span>
              Your credentials are securely processed.
            </span>
          </div>

          {/* Register */}
          <div className="auth-switch">
            <span>Don't have an account?</span>

            <Link to="/register">
              Create one
            </Link>
          </div>

        </div>

        <p className="auth-disclaimer">
          Educational finance assistant. Not professional
          financial, tax, or investment advice.
        </p>

      </div>
    </div>
  );
}

export default Login;
