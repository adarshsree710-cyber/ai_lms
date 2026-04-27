import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { api, getApiError } from "../lib/api";

function CourseDetailsPage() {
  const { courseId } = useParams();
  const { user } = useAuth();

  const [courseData, setCourseData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);
  const [completionMsg, setCompletionMsg] = useState("");

  useEffect(() => {
    loadCourse();
  }, [courseId]);

  async function loadCourse() {
    setError("");
    setLoading(true);
    try {
      const { data } = await api.get(`/courses/${courseId}`);
      setCourseData(data);
    } catch (err) {
      setError(getApiError(err, "Couldn't load this course."));
    } finally {
      setLoading(false);
    }
  }

  async function enroll() {
    setError("");
    setEnrolling(true);
    try {
      await api.post(`/courses/${courseId}/enroll`);
      await loadCourse(); // refresh to show enrolled state
    } catch (err) {
      setError(getApiError(err, "Couldn't enroll you in this course."));
    } finally {
      setEnrolling(false);
    }
  }

  async function markComplete() {
    setCompletionMsg("Saving...");
    try {
      await api.post("/progress/complete", { courseId });
      setCompletionMsg("Marked as complete!");
    } catch (err) {
      setCompletionMsg(getApiError(err, "Couldn't update completion status."));
    }
  }

  if (loading) {
    return (
      <section className="page-shell">
        <div className="panel">Loading course details...</div>
      </section>
    );
  }

  const course = courseData?.course;

  return (
    <section className="page-shell">
      {error && <div className="panel error-text">{error}</div>}

      <article className="panel course-detail-panel">
        <div className="page-header">
          <div>
            <p className="eyebrow">{course?.category || "Course"}</p>
            <h2>{course?.title}</h2>
          </div>
          <span className="badge">{course?.level || "Beginner"}</span>
        </div>

        <p className="muted-text">{course?.description}</p>
        <p className="muted-text">Instructor: {course?.instructor?.name || "Unknown"}</p>

        <div className="detail-actions">
          {user?.role === "student" && !courseData?.enrolled && (
            <button type="button" className="primary-button" onClick={enroll} disabled={enrolling}>
              {enrolling ? "Enrolling..." : "Enroll in course"}
            </button>
          )}
          {user?.role === "student" && courseData?.enrolled && (
            <button type="button" className="ghost-button" onClick={markComplete}>
              Mark complete
            </button>
          )}
        </div>

        {completionMsg && <p className="muted-text">{completionMsg}</p>}

        <div className="recommendation-box">
          <h3>AI recommendation</h3>
          <p className="muted-text">
            {course?.recommendation || "No recommendation available yet."}
          </p>
        </div>

        {course?.videoUrl ? (
          <div className="video-wrap">
            <iframe
              src={course.videoUrl}
              title={course.title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
        ) : (
          <div className="panel inline-panel">
            Video content is either hidden until you enroll, or this course doesn't have a video yet.
          </div>
        )}
      </article>
    </section>
  );
}

export default CourseDetailsPage;
