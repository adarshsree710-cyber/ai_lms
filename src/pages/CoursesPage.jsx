import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, getApiError } from "../lib/api";

const defaultFilters = { search: "", category: "", level: "" };

function CoursesPage() {
  const [filters, setFilters] = useState(defaultFilters);
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourses();
  }, []);

  async function fetchCourses(activeFilters = filters) {
    setError("");
    setLoading(true);
    try {
      // Strip out empty strings so we don't send ?search=&category= etc.
      const params = Object.fromEntries(
        Object.entries(activeFilters).filter(([, v]) => v)
      );
      const { data } = await api.get("/courses", { params });
      setCourses(data.courses || []);
    } catch (err) {
      setError(getApiError(err, "Couldn't load courses."));
    } finally {
      setLoading(false);
    }
  }

  function handleChange(e) {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSearch(e) {
    e.preventDefault();
    await fetchCourses(filters);
  }

  return (
    <section className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">Courses</p>
          <h2>Published learning paths</h2>
        </div>
      </div>

      <form className="panel filters-grid" onSubmit={handleSearch}>
        <input name="search" value={filters.search} onChange={handleChange} placeholder="Search courses" />
        <input name="category" value={filters.category} onChange={handleChange} placeholder="Category" />
        <select name="level" value={filters.level} onChange={handleChange}>
          <option value="">All levels</option>
          <option value="Beginner">Beginner</option>
          <option value="Intermediate">Intermediate</option>
          <option value="Advanced">Advanced</option>
        </select>
        <button type="submit" className="primary-button">Apply filters</button>
      </form>

      {error && <div className="panel error-text">{error}</div>}

      {loading ? (
        <div className="panel">Loading courses...</div>
      ) : (
        <div className="courses-grid">
          {courses.length === 0 && (
            <div className="panel">No published courses found.</div>
          )}
          {courses.map((course) => (
            <article key={course._id} className="course-card">
              <div className="course-thumb">
                {course.thumbnail ? (
                  <img src={course.thumbnail} alt={course.title} />
                ) : (
                  <div className="thumb-fallback">{course.title[0]}</div>
                )}
              </div>
              <div className="course-body">
                <div className="course-meta">
                  <span className="badge">{course.category || "General"}</span>
                  <span className="badge">{course.level || "Beginner"}</span>
                </div>
                <h3>{course.title}</h3>
                <p className="muted-text">{course.description}</p>
                <p className="muted-text">Instructor: {course.instructor?.name || "Unknown"}</p>
                <Link className="primary-button link-button" to={`/courses/${course._id}`}>
                  View details
                </Link>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

export default CoursesPage;
