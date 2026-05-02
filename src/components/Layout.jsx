import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Layout() {
  const { user, logout } = useAuth();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">AI LMS</p>
          <h1 className="brand-title">Learning cockpit</h1>
          <p className="muted-text">
            Track progress, manage courses, and enhance learning experiences with our AI-powered LMS.
          </p>
        </div>

        <nav className="nav-list">
          <NavLink to="/dashboard" className="nav-item">Dashboard</NavLink>
          <NavLink to="/courses" className="nav-item">Courses</NavLink>
          <NavLink to="/quiz" className="nav-item">Quiz Center</NavLink>
        </nav>

        <div className="profile-card">
          <p className="profile-name">{user?.name}</p>
          <p className="muted-text">
            {user?.email}
            <br />
            Role: {user?.role}
          </p>
          <button type="button" className="ghost-button" onClick={logout}>
            Sign out
          </button>
        </div>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;
