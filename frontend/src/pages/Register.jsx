import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ArrowRight, Eye, EyeOff, ShieldCheck, Sparkles } from "lucide-react";
import { registerUser } from "../services/api";

function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (!form.name.trim()) {
      setError("Please enter your name.");
      return;
    }

    if (!form.email.trim()) {
      setError("Please enter your email.");
      return;
    }

    if (form.password.length < 6) {
      setError("Password must contain at least 6 characters.");
      return;
    }

    try {
      setLoading(true);

      await registerUser(form);

      setSuccess("Account created successfully. Redirecting to login...");

      setTimeout(() => {
        navigate("/login");
      }, 1200);
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        "Unable to create account. Please try again.";

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-background-orb auth-orb-one"></div>
      <div className="auth-background-orb auth-orb-two"></div>

      <div className="auth-container">
        <div className="auth-brand">
          <Link to="/" className="auth-logo">
            <span className="logo-mark">F</span>
            FINOVA
          </Link>
        </div>

        <div className="auth-card">
          <div className="auth-card-header">
            <div className="auth-icon">
              <Sparkles size={20} />
            </div>

            <p className="auth-eyebrow">START YOUR JOURNEY</p>

            <h1>Create your account</h1>

            <p>
              Take control of your money with an intelligent finance
              assistant.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="input-group">
              <label htmlFor="name">Full name</label>

              <input
                id="name"
                name="name"
                type="text"
                placeholder="Enter your name"
                value={form.name}
                onChange={handleChange}
                autoComplete="name"
              />
            </div>

            <div className="input-group">
              <label htmlFor="email">Email address</label>

              <input
                id="email"
                name="email"
                type="email"
                placeholder="you@example.com"
                value={form.email}
                onChange={handleChange}
                autoComplete="email"
              />
            </div>

            <div className="input-group">
              <label htmlFor="password">Password</label>

              <div className="password-wrapper">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Create a secure password"
                  value={form.password}
                  onChange={handleChange}
                  autoComplete="new-password"
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={
                    showPassword ? "Hide password" : "Show password"
                  }
                >
                  {showPassword ? (
                    <EyeOff size={18} />
                  ) : (
                    <Eye size={18} />
                  )}
                </button>
              </div>
            </div>

            {error && <div className="auth-message error">{error}</div>}

            {success && (
              <div className="auth-message success">{success}</div>
            )}

            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >
              {loading ? (
                "Creating account..."
              ) : (
                <>
                  Create account
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          <div className="auth-security">
            <ShieldCheck size={17} />

            <span>
              Your password is securely hashed before storage.
            </span>
          </div>

          <div className="auth-switch">
            Already have an account?
            <Link to="/login">Sign in</Link>
          </div>
        </div>

        <p className="auth-footer">
          © 2026 FINOVA · AI Finance Assistant
        </p>
      </div>
    </div>
  );
}

export default Register;