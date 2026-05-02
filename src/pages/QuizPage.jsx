import { useEffect, useState } from "react";
import { api, getApiError } from "../lib/api";

function QuizPage() {
  const [quizzes, setQuizzes] = useState([]);
  const [selectedId, setSelectedId] = useState("");
  const [quiz, setQuiz] = useState(null);
  const [score, setScore] = useState(80);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadQuizList();
  }, []);

  useEffect(() => {
    if (!selectedId) {
      setQuiz(null);
      return;
    }
    loadQuizDetails(selectedId);
  }, [selectedId]);

  async function loadQuizList() {
    setError("");
    setLoading(true);
    try {
      const { data } = await api.get("/quiz");
      setQuizzes(data.quizzes || []);
      // Auto-select the first quiz if there is one
      if (data.quizzes?.[0]?._id) {
        setSelectedId(data.quizzes[0]._id);
      }
    } catch (err) {
      setError(getApiError(err, "Couldn't load quizzes."));
    } finally {
      setLoading(false);
    }
  }

  async function loadQuizDetails(id) {
    try {
      const { data } = await api.get(`/quiz/${id}`);
      setQuiz(data.quiz);
      setResult(null); // clear any previous result when switching quizzes
    } catch (err) {
      setError(getApiError(err, "Couldn't load quiz details."));
    }
  }

  async function submitQuiz() {
    if (!quiz) return;

    setError("");
    setSubmitting(true);
    try {
      const { data } = await api.post("/quiz", {
        score: Number(score),
        quizId: quiz._id,
        courseId: quiz.course?._id,
      });
      setResult(data.result);
    } catch (err) {
      setError(getApiError(err, "Couldn't submit your quiz."));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">Quiz Center</p>
          <h2>Take a quiz and sync your progress</h2>
        </div>
      </div>

      {error && <div className="panel error-text">{error}</div>}

      {loading ? (
        <div className="panel">Loading quizzes...</div>
      ) : (
        <>
          <article className="panel">
            <label>
              Choose quiz
              <select value={selectedId} onChange={(e) => setSelectedId(e.target.value)}>
                {quizzes.map((q) => (
                  <option key={q._id} value={q._id}>{q.title}</option>
                ))}
              </select>
            </label>
          </article>

          {quiz && (
            <article className="panel">
              <div className="page-header">
                <div>
                  <h3>{quiz.title}</h3>
                  <p className="muted-text">
                    Course: {quiz.course?.title || "Unknown"} &nbsp;|&nbsp; Passing score: {quiz.passingScore}%
                  </p>
                </div>
              </div>

              <div className="panel inline-panel">
                The backend expects a score submission. Enter the score you want to record for this attempt.
              </div>

              <label>
                Score
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={score}
                  onChange={(e) => setScore(e.target.value)}
                />
              </label>

              <div className="questions-list">
                {quiz.questions.map((q, i) => (
                  <div key={q._id || i} className="question-card">
                    <p><strong>{i + 1}. {q.text}</strong></p>
                    <div className="options-list">
                      {q.options.map((opt, j) => (
                        <div key={`${q._id || i}-${j}`} className="option-row">
                          <span>{opt}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              <button
                type="button"
                className="primary-button"
                onClick={submitQuiz}
                disabled={submitting}
              >
                {submitting ? "Submitting..." : "Submit quiz"}
              </button>
            </article>
          )}

          {result && (
            <article className="panel result-panel">
              <h3>Submission result</h3>
              <p className="result-score">{result.score}%</p>
              <p className="muted-text">Average score: {result.averageScore}%</p>
              <p className={`badge ${result.passed ? "badge-success" : "badge-warning"}`}>
                {result.passed ? "Passed" : "Needs review"}
              </p>
              <p className="muted-text">{result.aiFeedback}</p>
            </article>
          )}
        </>
      )}
    </section>
  );
}

export default QuizPage;
