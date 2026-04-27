import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { api, getApiError } from "../lib/api";

function RegisterPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      const { data } = await api.post("/register", { name, email, password, role });
      login(data);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(getApiError(err, "Couldn't create your account."));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-shell">
      <section className="auth-hero">
        <p className="eyebrow">Join the platform</p>
        <h1>Start learning with the same API your backend exposes.</h1>
        <p className="muted-text">
          Registration sends <code>name</code>, <code>email</code>, <code>password</code>,
          and <code>role</code> to <code>/api/register</code>.
        </p>
      </section>

      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Create account</h2>

        <label>
          Full name
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="John Doe"
            required
          />
        </label>

        <label>
          Email
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="john@example.com"
            required
          />
        </label>

        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="at least 6 characters"
            minLength={6}
            required
          />
        </label>

        <label>
          Role
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="student">Student</option>
            <option value="instructor">Instructor</option>
            <option value="admin">Admin</option>
          </select>
        </label>

        {error && <p className="error-text">{error}</p>}

        <button type="submit" className="primary-button" disabled={submitting}>
          {submitting ? "Creating account..." : "Create account"}
        </button>

        <p className="muted-text">
          Already registered? <Link to="/login">Go to login</Link>
        </p>
      </form>
    </div>
  );
}

export default RegisterPage;
