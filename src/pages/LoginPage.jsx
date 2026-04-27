import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { api, getApiError } from "../lib/api";

function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const redirectTo = location.state?.from?.pathname || "/dashboard";

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      const { data } = await api.post("/login", { email, password });
      login(data);
      navigate(redirectTo, { replace: true });
    } catch (err) {
      setError(getApiError(err, "Couldn't sign you in."));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-shell">
      <section className="auth-hero">
        <p className="eyebrow">AI Learning management system </p>
        <h1>Welcome to the <br/>
          AI Learning 
          <br/>Platform</h1>
        <p className="muted-text">
          Sign in with one of the seeded accounts below to try everything out.
        </p>
        {/* <div className="demo-box">
          <p><strong>Student:</strong> student@ailms.com / password123</p>
          <p><strong>Instructor:</strong> instructor@ailms.com / password123</p>
          <p><strong>Admin:</strong> admin@ailms.com / password123</p>
        </div> */}
      </section>

      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Login</h2>

        <label>
          Email
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="student@ailms.com"
            required
          />
        </label>

        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="password123"
            required
          />
        </label>

        {error && <p className="error-text">{error}</p>}

        <button type="submit" className="primary-button" disabled={submitting}>
          {submitting ? "Signing in..." : "Sign in"}
        </button>

        <p className="muted-text">
          No account yet? <Link to="/register">Create one</Link>
        </p>
      </form>
    </div>
  );
}

export default LoginPage;
