import { useEffect, useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import StatCard from "../components/StatCard";
import { useAuth } from "../context/AuthContext";
import { api, getApiError } from "../lib/api";

// ─── helpers ────────────────────────────────────────────────────────────────

function toArray(val) {
  return Array.isArray(val) ? val : [];
}

// Find the first value that's actually a finite number
function firstNumber(...vals) {
  const found = vals.find((v) => Number.isFinite(Number(v)));
  return found === undefined ? null : Number(found);
}

// Find the first non-empty string
function firstText(...vals) {
  return vals.find((v) => typeof v === "string" && v.trim()) || "";
}

// ─── normalizers ─────────────────────────────────────────────────────────────

// The backend can return student data in a bunch of different shapes — this
// flattens everything into a consistent object we can actually render.
function normalizeStudent(raw, fallbackCourse = "Assigned course") {
  const scores = toArray(
    raw?.quizScores || raw?.scores || raw?.results || raw?.attempts
  );

  const avgFromScores = scores.length
    ? scores.reduce((sum, s) => sum + Number(s?.score ?? s ?? 0), 0) / scores.length
    : null;

  const avgScore =
    firstNumber(raw?.averageScore, raw?.avgScore, raw?.score, raw?.progress?.score, avgFromScores) ?? 0;

  const progress = firstNumber(
    raw?.progressPercentage,
    raw?.completionRate,
    raw?.progress,
    raw?.completedPercentage
  );

  return {
    id: raw?._id || raw?.id || raw?.email || `${fallbackCourse}-${raw?.name || "student"}`,
    name: firstText(raw?.name, raw?.fullName, raw?.user?.name) || "Unknown student",
    email: firstText(raw?.email, raw?.user?.email) || "Email unavailable",
    courseTitle: firstText(raw?.courseTitle, raw?.course?.title, fallbackCourse),
    avgScore: Math.round(avgScore),
    progress: progress === null ? null : Math.round(progress),
    status:
      firstText(raw?.status, raw?.progressStatus) ||
      (avgScore >= 75 ? "Performing well" : avgScore >= 50 ? "Needs support" : "At risk"),
    quizCount: firstNumber(raw?.totalQuizzes, raw?.quizCount, scores.length) ?? 0,
  };
}

// Pull students out of nested course data when the backend doesn't give us a
// flat list
function studentsFromCourses(courses) {
  return courses.flatMap((course) => {
    const nested = [
      ...toArray(course?.students),
      ...toArray(course?.learners),
      ...toArray(course?.enrollments).map((e) => e?.student || e?.user || e),
    ];
    return nested.map((s) => normalizeStudent(s, course?.title || "Assigned course"));
  });
}

// Build the instructor dashboard from whatever the various endpoints returned
function buildInstructorData(coursesRes, extras) {
  const courses = toArray(coursesRes?.courses || coursesRes);

  const withStudents = extras.find(
    (p) =>
      toArray(p?.students).length ||
      toArray(p?.studentDetails).length ||
      toArray(p?.learners).length
  );

  const rawStudents = [
    ...toArray(withStudents?.students),
    ...toArray(withStudents?.studentDetails),
    ...toArray(withStudents?.learners),
  ];

  const normalized = (
    rawStudents.length ? rawStudents.map((s) => normalizeStudent(s)) : studentsFromCourses(courses)
  ).filter(Boolean);

  // Deduplicate by id, keeping the best data for each student
  const byId = new Map();
  for (const s of normalized) {
    if (!byId.has(s.id)) {
      byId.set(s.id, s);
      continue;
    }
    const existing = byId.get(s.id);
    byId.set(s.id, {
      ...existing,
      courseTitle: existing.courseTitle === "Assigned course" ? s.courseTitle : existing.courseTitle,
      avgScore: Math.max(existing.avgScore, s.avgScore),
      quizCount: Math.max(existing.quizCount, s.quizCount),
      progress: existing.progress ?? s.progress,
      status: existing.status === "At risk" ? existing.status : s.status,
    });
  }

  const students = Array.from(byId.values());
  const scored = students.filter((s) => Number.isFinite(s.avgScore));
  const classAvg = scored.length
    ? Math.round(scored.reduce((sum, s) => sum + s.avgScore, 0) / scored.length)
    : 0;

  return {
    courses,
    students,
    totalCourses: firstNumber(withStudents?.totalCourses, courses.length) ?? courses.length,
    totalStudents: firstNumber(withStudents?.totalStudents, students.length) ?? students.length,
    classAvg,
    topPerformers: [...students].sort((a, b) => b.avgScore - a.avgScore).slice(0, 5),
    needsAttention: students
      .filter((s) => s.avgScore < 60 || (s.progress !== null && s.progress < 50))
      .slice(0, 5),
  };
}

// ─── component ───────────────────────────────────────────────────────────────

function DashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadDashboard();
  }, [user?.role]);

  async function loadDashboard() {
    setError("");
    setLoading(true);
    try {
      if (user?.role === "instructor") {
        // Fire all instructor requests in parallel; the optional ones are
        // allowed to fail without taking down the whole page
        const [coursesRes, ...optionals] = await Promise.all([
          api.get("/courses"),
          api.get("/instructor/dashboard").catch(() => null),
          api.get("/instructor/students").catch(() => null),
          api.get("/progress").catch(() => null),
        ]);

        const payloads = optionals.map((r) => r?.data).filter(Boolean);
        setData(buildInstructorData(coursesRes.data, payloads));
      } else {
        const { data: res } = await api.get("/progress");
        setData(res);
      }
    } catch (err) {
      setError(getApiError(err, "Couldn't load dashboard data."));
    } finally {
      setLoading(false);
    }
  }

  async function refreshRecommendation() {
    // Instructors just reload; students hit the AI endpoint
    if (user?.role === "instructor") {
      await loadDashboard();
      return;
    }

    setRefreshing(true);
    try {
      const { data: res } = await api.post("/progress/ai-recommendation");
      setData((prev) =>
        prev
          ? { ...prev, recommendation: res.recommendation, score: res.score, completed: res.completed }
          : prev
      );
    } catch (err) {
      setError(getApiError(err, "Couldn't refresh recommendation."));
    } finally {
      setRefreshing(false);
    }
  }

  const chartData = (data?.chartScores || []).map((score, i) => ({
    name: `Quiz ${i + 1}`,
    score,
  }));

  if (loading) {
    return (
      <section className="page-shell">
        <div className="panel">Loading dashboard...</div>
      </section>
    );
  }

  return (
    <section className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">Dashboard</p>
          <h2>{user?.role === "instructor" ? "Instructor control center" : "Your progress snapshot"}</h2>
        </div>
        <button type="button" className="ghost-button" onClick={refreshRecommendation} disabled={refreshing}>
          {refreshing
            ? "Refreshing..."
            : user?.role === "instructor"
            ? "Refresh class insights"
            : "Refresh AI recommendation"}
        </button>
      </div>

      {error && <div className="panel error-text">{error}</div>}

      {user?.role === "instructor" ? (
        <InstructorView data={data} />
      ) : (
        <StudentView data={data} chartData={chartData} />
      )}
    </section>
  );
}

// ─── instructor view ──────────────────────────────────────────────────────────

function InstructorView({ data }) {
  return (
    <>
      <div className="stats-grid">
        <StatCard label="Courses managed" value={data?.totalCourses ?? 0} hint="Pulled from published course data" />
        <StatCard label="Students tracked" value={data?.totalStudents ?? 0} hint="Unique learners across your courses" />
        <StatCard label="Class average" value={`${data?.classAvg ?? 0}%`} hint="Computed from available student scores" />
      </div>

      <div className="dashboard-grid">
        <article className="panel">
          <h3>Top performers</h3>
          {data?.topPerformers?.length ? (
            <div className="stack-list">
              {data.topPerformers.map((s) => (
                <div key={s.id} className="list-card">
                  <div>
                    <strong>{s.name}</strong>
                    <p className="muted-text student-subtext">{s.email} | {s.courseTitle}</p>
                  </div>
                  <span className="badge badge-success">{s.avgScore}%</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="muted-text">Student score data isn't available from the backend yet.</p>
          )}
        </article>

        <article className="panel">
          <h3>Needs attention</h3>
          {data?.needsAttention?.length ? (
            <div className="stack-list">
              {data.needsAttention.map((s) => (
                <div key={s.id} className="list-card">
                  <div>
                    <strong>{s.name}</strong>
                    <p className="muted-text student-subtext">
                      {s.courseTitle} | {s.quizCount} quiz attempts
                    </p>
                  </div>
                  <span className="badge badge-warning">{s.avgScore}%</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="muted-text">No low-scoring students in the current dataset.</p>
          )}
        </article>
      </div>

      <article className="panel">
        <h3>Student details</h3>
        {data?.students?.length ? (
          <div className="student-list">
            {data.students.map((s) => (
              <div key={s.id} className="student-row">
                <div>
                  <strong>{s.name}</strong>
                  <p className="muted-text student-subtext">{s.email}</p>
                </div>
                <div>
                  <strong>{s.courseTitle}</strong>
                  <p className="muted-text student-subtext">
                    {s.quizCount} quizzes
                    {s.progress !== null ? ` | ${s.progress}% progress` : ""}
                  </p>
                </div>
                <div className="student-metrics">
                  <span className={`badge ${s.avgScore >= 75 ? "badge-success" : "badge-warning"}`}>
                    Score {s.avgScore}%
                  </span>
                  <span className="badge">{s.status}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="muted-text">
            Student details will show up once your backend returns enrolled learner data for instructor accounts.
          </p>
        )}
      </article>
    </>
  );
}

// ─── student view ─────────────────────────────────────────────────────────────

function StudentView({ data, chartData }) {
  return (
    <>
      <div className="stats-grid">
        <StatCard label="Completed courses" value={data?.completed ?? 0} hint="Tracked from /api/progress" />
        <StatCard
          label="Average score"
          value={`${data?.score ?? 0}%`}
          hint={`${data?.totalQuizzes ?? 0} quizzes submitted`}
        />
        <StatCard
          label="Last updated"
          value={data?.lastUpdated ? new Date(data.lastUpdated).toLocaleDateString() : "N/A"}
          hint="Pulled from backend progress record"
        />
      </div>

      <div className="dashboard-grid">
        <article className="panel">
          <h3>Study recommendation</h3>
          <p className="muted-text">
            {data?.recommendation || "No recommendation yet. Submit a quiz or refresh once the AI service is set up."}
          </p>
        </article>

        <article className="panel">
          <h3>Recent performance</h3>
          {chartData.length ? (
            <div className="chart-wrap">
              <ResponsiveContainer width="100%" height={260}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="name" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" domain={[0, 100]} />
                  <Tooltip />
                  <Line type="monotone" dataKey="score" stroke="#f97316" strokeWidth={3} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p className="muted-text">No quiz history yet — take a quiz to populate this chart.</p>
          )}
        </article>
      </div>

      <div className="dashboard-grid">
        <article className="panel">
          <h3>Tracked courses</h3>
          {data?.courses?.length ? (
            <div className="stack-list">
              {data.courses.map((entry) => (
                <div key={entry._id || entry.course?._id} className="list-card">
                  <strong>{entry.course?.title || "Untitled course"}</strong>
                  <span className="badge">{entry.completed ? "Completed" : "In progress"}</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="muted-text">You haven't enrolled in any courses yet.</p>
          )}
        </article>

        <article className="panel">
          <h3>Recent quiz attempts</h3>
          {data?.quizScores?.length ? (
            <div className="stack-list">
              {data.quizScores
                .slice(-5)
                .reverse()
                .map((entry) => (
                  <div key={entry._id} className="list-card">
                    <strong>{entry.quiz?.title || "Quiz attempt"}</strong>
                    <span className={`badge ${entry.passed ? "badge-success" : "badge-warning"}`}>
                      {entry.score}%
                    </span>
                  </div>
                ))}
            </div>
          ) : (
            <p className="muted-text">No quiz attempts yet.</p>
          )}
        </article>
      </div>
    </>
  );
}

export default DashboardPage;
