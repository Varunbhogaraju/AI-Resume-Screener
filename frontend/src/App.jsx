import { useEffect, useState } from "react";
import axios from "axios";
import {
  LayoutDashboard,
  BriefcaseBusiness,
  Users,
  FileSearch,
  LogOut,
  Plus,
  Search,
  CheckCircle2,
  XCircle,
  Sparkles,
  ArrowUpRight,
  UserPlus,
} from "lucide-react";
import "./App.css";

const API = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API,
});

function App() {
  const [page, setPage] = useState("dashboard");
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(localStorage.getItem("user") || "");

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setToken(null);
    setUser("");
  };

  if (!token) {
    return (
      <Auth
        onLogin={(newToken, username) => {
          localStorage.setItem("token", newToken);
          localStorage.setItem("user", username || "Recruiter");
          setToken(newToken);
          setUser(username || "Recruiter");
        }}
      />
    );
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Sparkles size={20} />
          </div>

          <div>
            <div className="brand-title">ResumeAI</div>
            <div className="brand-subtitle">Smart Screening</div>
          </div>
        </div>

        <nav className="nav">
          <NavItem
            icon={<LayoutDashboard size={18} />}
            label="Dashboard"
            active={page === "dashboard"}
            onClick={() => setPage("dashboard")}
          />

          <NavItem
            icon={<BriefcaseBusiness size={18} />}
            label="Jobs"
            active={page === "jobs"}
            onClick={() => setPage("jobs")}
          />

          <NavItem
            icon={<Users size={18} />}
            label="Candidates"
            active={page === "candidates"}
            onClick={() => setPage("candidates")}
          />

          <NavItem
            icon={<FileSearch size={18} />}
            label="Screen Candidate"
            active={page === "screen"}
            onClick={() => setPage("screen")}
          />
        </nav>

        <div className="sidebar-bottom">
          <div className="user-mini">
            <div className="avatar">
              {(user || "R")[0].toUpperCase()}
            </div>

            <div className="user-info">
              <strong>{user || "Recruiter"}</strong>
              <span>Recruiter</span>
            </div>
          </div>

          <button className="logout-btn" onClick={logout}>
            <LogOut size={17} />
            Logout
          </button>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <div className="eyebrow">AI-POWERED RECRUITMENT</div>

            <h1>
              {page === "dashboard" && "Dashboard"}
              {page === "jobs" && "Jobs"}
              {page === "candidates" && "Candidates"}
              {page === "screen" && "Screen Candidate"}
            </h1>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            AI Engine Online
          </div>
        </header>

        {page === "dashboard" && <Dashboard setPage={setPage} />}

        {page === "jobs" && <Jobs setPage={setPage} />}

        {page === "candidates" && <Candidates />}

        {page === "screen" && <ScreenCandidate />}
      </main>
    </div>
  );
}

function Auth({ onLogin }) {
  const [mode, setMode] = useState("signup");
  const [signupEmail, setSignupEmail] = useState("");

  const showLogin = (email = "") => {
    if (email) {
      setSignupEmail(email);
    }

    setMode("login");
  };

  if (mode === "signup") {
    return (
      <Signup
        onBack={(email) => showLogin(email)}
      />
    );
  }

  return (
    <Login
      email={signupEmail}
      setEmail={setSignupEmail}
      onLogin={onLogin}
      onSignup={() => setMode("signup")}
    />
  );
}

function Login({
  email,
  setEmail,
  onLogin,
  onSignup,
}) {
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const login = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");

    try {
      const response = await api.post(
        "/api/v1/auth/login",
        {
          email,
          password,
        }
      );

      onLogin(
        response.data.access_token,
        email
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Login failed. Check your email and password."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-left">
        <div className="login-brand">
          <div className="brand-icon">
            <Sparkles size={22} />
          </div>

          <span>ResumeAI</span>
        </div>

        <div className="hero-copy">
          <div className="hero-pill">
            <Sparkles size={15} />
            AI-powered recruitment
          </div>

          <h1>
            Find the right
            <br />
            <span>candidate faster.</span>
          </h1>

          <p>
            Screen resumes intelligently using AI-powered
            skill matching, experience analysis and semantic
            job relevance.
          </p>
        </div>

        <div className="login-features">
          <Feature
            title="AI Resume Analysis"
            text="Extract skills, experience and candidate information."
          />

          <Feature
            title="Semantic Matching"
            text="Understand relevant experience beyond simple keywords."
          />

          <Feature
            title="Explainable Results"
            text="See matched skills, missing skills and recommendations."
          />
        </div>
      </div>

      <div className="login-right">
        <form className="login-card" onSubmit={login}>
          <div className="login-card-heading">
            <h2>Welcome back</h2>

            <p>
              Sign in to your recruitment workspace.
            </p>
          </div>

          <label>Email</label>

          <input
            type="email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            placeholder="Enter email"
            required
          />

          <label>Password</label>

          <input
            type="password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            placeholder="Enter password"
            required
          />

          {error && (
            <div className="error-box">
              {error}
            </div>
          )}

          <button
            className="primary-btn full"
            disabled={loading}
          >
            {loading
              ? "Signing in..."
              : "Sign in"}
          </button>

          <div className="auth-switch">
            Don't have an account?{" "}
            <button
              type="button"
              onClick={onSignup}
            >
              Create account
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function Signup({ onBack }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const register = async (e) => {
    e.preventDefault();

    setError("");

    const formData = new FormData(e.currentTarget);

    const name = formData.get("name");
    const email = formData.get("email");
    const password = formData.get("password");
    const confirmPassword =
      formData.get("confirmPassword");

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    if (password.length < 8) {
      setError(
        "Password must contain at least 8 characters."
      );
      return;
    }

    setLoading(true);

    try {
      await api.post(
        "/api/v1/auth/register",
        {
          name,
          email,
          password,
        }
      );

      onBack(email);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Registration failed."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-left">
        <div className="login-brand">
          <div className="brand-icon">
            <UserPlus size={22} />
          </div>

          <span>ResumeAI</span>
        </div>

        <div className="hero-copy">
          <div className="hero-pill">
            <Sparkles size={15} />
            Intelligent candidate screening
          </div>

          <h1>
            Build your
            <br />
            <span>recruitment workspace.</span>
          </h1>

          <p>
            Create your recruiter account and start
            screening candidates with AI-powered analysis.
          </p>
        </div>

        <div className="login-features">
          <Feature
            title="Smart Resume Analysis"
            text="Extract structured candidate information from resumes."
          />

          <Feature
            title="Semantic Matching"
            text="Compare candidate experience with real job requirements."
          />

          <Feature
            title="Actionable Results"
            text="Identify strengths, gaps and hiring recommendations."
          />
        </div>
      </div>

      <div className="login-right">
        <form
          className="login-card"
          onSubmit={register}
        >
          <div className="login-card-heading">
            <h2>Create account</h2>

            <p>
              Set up your recruiter workspace.
            </p>
          </div>

          <label>Full name</label>

          <input
            type="text"
            name="name"
            placeholder="Enter your name"
            minLength="2"
            maxLength="120"
            required
          />

          <label>Email</label>

          <input
            type="email"
            name="email"
            placeholder="Enter email"
            required
          />

          <label>Password</label>

          <input
            type="password"
            name="password"
            placeholder="Minimum 8 characters"
            minLength="8"
            maxLength="128"
            required
          />

          <label>Confirm password</label>

          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm password"
            minLength="8"
            maxLength="128"
            required
          />

          {error && (
            <div className="error-box">
              {error}
            </div>
          )}

          <button
            className="primary-btn full"
            disabled={loading}
          >
            {loading
              ? "Creating account..."
              : "Create account"}
          </button>

          <div className="auth-switch">
            Already have an account?{" "}
            <button
              type="button"
              onClick={() => onBack()}
            >
              Sign in
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function Dashboard({ setPage }) {
  const [jobs, setJobs] = useState([]);
  const [candidates, setCandidates] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const token =
        localStorage.getItem("token");

      const headers = {
        Authorization: `Bearer ${token}`,
      };

      const [
        jobsResponse,
        candidatesResponse,
      ] = await Promise.all([
        api.get("/api/v1/jobs", {
          headers,
        }),
        api.get(
          "/api/v1/candidates",
          {
            headers,
          }
        ),
      ]);

      setJobs(
        Array.isArray(jobsResponse.data)
          ? jobsResponse.data
          : []
      );

      setCandidates(
        Array.isArray(
          candidatesResponse.data
        )
          ? candidatesResponse.data
          : []
      );
    } catch {
      setJobs([]);
      setCandidates([]);
    }
  };

  return (
    <>
      <section className="welcome">
        <div>
          <h2>Good to see you.</h2>

          <p>
            Here's an overview of your recruitment activity.
          </p>
        </div>

        <button
          className="primary-btn"
          onClick={() => setPage("screen")}
        >
          <FileSearch size={17} />
          Screen candidate
        </button>
      </section>

      <section className="stats-grid">
        <StatCard
          icon={
            <BriefcaseBusiness size={20} />
          }
          label="Active Jobs"
          value={jobs.length}
        />

        <StatCard
          icon={<Users size={20} />}
          label="Candidates"
          value={candidates.length}
        />

        <StatCard
          icon={<FileSearch size={20} />}
          label="AI Screenings"
          value="—"
        />

        <StatCard
          icon={<Sparkles size={20} />}
          label="AI Engine"
          value="Online"
          small
        />
      </section>

      <section className="dashboard-grid">
        <div className="panel">
          <div className="panel-heading">
            <div>
              <h3>Recruitment workflow</h3>

              <p>
                Go from job description to candidate
                recommendation.
              </p>
            </div>
          </div>

          <div className="workflow">
            <WorkflowStep
              number="01"
              title="Create a job"
              text="Define the role, skills and experience requirements."
            />

            <WorkflowStep
              number="02"
              title="Add candidates"
              text="Upload resumes and build your candidate pool."
            />

            <WorkflowStep
              number="03"
              title="Run AI screening"
              text="Combine deterministic and semantic AI matching."
            />

            <WorkflowStep
              number="04"
              title="Review results"
              text="See scores, matched skills and missing requirements."
            />
          </div>
        </div>

        <div className="panel quick-panel">
          <div className="panel-heading">
            <div>
              <h3>Quick actions</h3>

              <p>
                Start your next screening workflow.
              </p>
            </div>
          </div>

          <button
            className="quick-action"
            onClick={() => setPage("jobs")}
          >
            <div className="quick-icon">
              <Plus size={18} />
            </div>

            <div>
              <strong>Create job</strong>

              <span>
                Add a new recruitment requirement.
              </span>
            </div>

            <ArrowUpRight size={17} />
          </button>

          <button
            className="quick-action"
            onClick={() =>
              setPage("candidates")
            }
          >
            <div className="quick-icon">
              <Users size={18} />
            </div>

            <div>
              <strong>View candidates</strong>

              <span>
                Review your candidate pool.
              </span>
            </div>

            <ArrowUpRight size={17} />
          </button>

          <button
            className="quick-action"
            onClick={() =>
              setPage("screen")
            }
          >
            <div className="quick-icon">
              <FileSearch size={18} />
            </div>

            <div>
              <strong>Screen candidate</strong>

              <span>
                Run AI-powered candidate screening.
              </span>
            </div>

            <ArrowUpRight size={17} />
          </button>
        </div>
      </section>
    </>
  );
}

function Jobs({ setPage }) {
  const [jobs, setJobs] = useState([]);
  const [showForm, setShowForm] =
    useState(false);

  const [form, setForm] = useState({
    title: "",
    description: "",
    required_skills: "",
    experience_requirement: "",
  });

  const [message, setMessage] =
    useState("");

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = async () => {
    try {
      const token =
        localStorage.getItem("token");

      const response = await api.get(
        "/api/v1/jobs",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setJobs(
        Array.isArray(response.data)
          ? response.data
          : []
      );
    } catch {
      setJobs([]);
    }
  };

  const createJob = async (e) => {
    e.preventDefault();

    setMessage("");

    try {
      const token =
        localStorage.getItem("token");

      await api.post(
        "/api/v1/jobs",
        form,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setMessage(
        "Job created successfully."
      );

      setForm({
        title: "",
        description: "",
        required_skills: "",
        experience_requirement: "",
      });

      setShowForm(false);

      loadJobs();
    } catch (err) {
      setMessage(
        err.response?.data?.detail ||
          "Unable to create job."
      );
    }
  };

  return (
    <>
      <div className="page-actions">
        <div>
          <button
            className="secondary-btn"
            onClick={() =>
              setPage("dashboard")
            }
          >
            ← Back to Dashboard
          </button>

          <p className="page-description">
            Manage your open positions and requirements.
          </p>
        </div>

        <button
          className="primary-btn"
          onClick={() =>
            setShowForm(!showForm)
          }
        >
          <Plus size={17} />
          New job
        </button>
      </div>

      {message && (
        <div className="success-box">
          {message}
        </div>
      )}

      {showForm && (
        <form
          className="panel form-panel"
          onSubmit={createJob}
        >
          <h3>Create job</h3>

          <div className="form-grid">
            <div>
              <label>Job title</label>

              <input
                value={form.title}
                onChange={(e) =>
                  setForm({
                    ...form,
                    title: e.target.value,
                  })
                }
                required
              />
            </div>

            <div>
              <label>
                Experience requirement
              </label>

              <input
                value={
                  form.experience_requirement
                }
                onChange={(e) =>
                  setForm({
                    ...form,
                    experience_requirement:
                      e.target.value,
                  })
                }
                placeholder="e.g. 2 years"
              />
            </div>
          </div>

          <label>Required skills</label>

          <input
            value={form.required_skills}
            onChange={(e) =>
              setForm({
                ...form,
                required_skills:
                  e.target.value,
              })
            }
            placeholder="Python, FastAPI, SQL, Docker"
            required
          />

          <label>Job description</label>

          <textarea
            value={form.description}
            onChange={(e) =>
              setForm({
                ...form,
                description:
                  e.target.value,
              })
            }
            rows="5"
            required
          />

          <div className="form-actions">
            <button
              type="button"
              className="secondary-btn"
              onClick={() =>
                setShowForm(false)
              }
            >
              Cancel
            </button>

            <button className="primary-btn">
              Create job
            </button>
          </div>
        </form>
      )}

      <div className="panel">
        <div className="panel-heading">
          <div>
            <h3>Open positions</h3>

            <p>
              {jobs.length} jobs available
            </p>
          </div>
        </div>

        {jobs.length === 0 ? (
          <EmptyState
            icon={
              <BriefcaseBusiness size={22} />
            }
            title="No jobs yet"
            text="Create your first job requirement to start screening."
          />
        ) : (
          <div className="job-list">
            {jobs.map((job) => (
              <div
                className="job-row"
                key={job.id}
              >
                <div className="job-icon">
                  <BriefcaseBusiness
                    size={19}
                  />
                </div>

                <div className="job-main">
                  <strong>
                    {job.title ||
                      `Job #${job.id}`}
                  </strong>

                  <span>
                    {job.required_skills ||
                      "No skills specified"}
                  </span>
                </div>

                <div className="job-id">
                  #{job.id}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}

function Candidates() {
  const [candidates, setCandidates] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    loadCandidates();
  }, []);

  const loadCandidates = async () => {
    try {
      const token =
        localStorage.getItem("token");

      const response = await api.get(
        "/api/v1/candidates",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setCandidates(
        Array.isArray(response.data)
          ? response.data
          : []
      );
    } catch {
      setCandidates([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="page-actions">
        <p className="page-description">
          Candidate profiles and uploaded resumes.
        </p>
      </div>

      <div className="panel">
        <div className="panel-heading">
          <div>
            <h3>Candidate pool</h3>

            <p>
              {candidates.length} candidates
              in the system
            </p>
          </div>

          <div className="search-box">
            <Search size={16} />

            <input
              placeholder="Search candidates..."
            />
          </div>
        </div>

        {loading ? (
          <div className="empty-state">
            Loading...
          </div>
        ) : candidates.length === 0 ? (
          <EmptyState
            icon={<Users size={22} />}
            title="No candidates yet"
            text="Upload a resume to add your first candidate."
          />
        ) : (
          <div className="candidate-list">
            {candidates.map(
              (candidate) => (
                <div
                  className="candidate-row"
                  key={candidate.id}
                >
                  <div className="avatar candidate-avatar">
                    {(
                      candidate.name ||
                      candidate.email ||
                      "C"
                    )[0].toUpperCase()}
                  </div>

                  <div className="candidate-main">
                    <strong>
                      {candidate.name ||
                        `Candidate #${candidate.id}`}
                    </strong>

                    <span>
                      {candidate.email ||
                        "Resume uploaded"}
                    </span>
                  </div>

                  <div className="candidate-id">
                    #{candidate.id}
                  </div>
                </div>
              )
            )}
          </div>
        )}
      </div>
    </>
  );
}

function ScreenCandidate() {
  const [jobs, setJobs] = useState([]);
  const [candidates, setCandidates] =
    useState([]);

  const [jobId, setJobId] =
    useState("");

  const [candidateId, setCandidateId] =
    useState("");

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  useEffect(() => {
    loadOptions();
  }, []);

  const loadOptions = async () => {
    try {
      const token =
        localStorage.getItem("token");

      const headers = {
        Authorization: `Bearer ${token}`,
      };

      const [
        jobsResponse,
        candidatesResponse,
      ] = await Promise.all([
        api.get("/api/v1/jobs", {
          headers,
        }),
        api.get(
          "/api/v1/candidates",
          {
            headers,
          }
        ),
      ]);

      const jobsData =
        Array.isArray(
          jobsResponse.data
        )
          ? jobsResponse.data
          : [];

      const candidatesData =
        Array.isArray(
          candidatesResponse.data
        )
          ? candidatesResponse.data
          : [];

      setJobs(jobsData);
      setCandidates(candidatesData);

      if (jobsData.length > 0) {
        setJobId(
          String(jobsData[0].id)
        );
      }

      if (candidatesData.length > 0) {
        setCandidateId(
          String(
            candidatesData[0].id
          )
        );
      }
    } catch {
      setJobs([]);
      setCandidates([]);
    }
  };

  const screen = async (e) => {
    e.preventDefault();

    if (!jobId || !candidateId) {
      setError(
        "Please select a job and candidate."
      );
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const token =
        localStorage.getItem("token");

      const response = await api.post(
        `/api/v1/jobs/${jobId}/candidates/${candidateId}/screen`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setResult(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Screening failed."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="page-actions">
        <p className="page-description">
          Run AI-powered semantic screening against a job.
        </p>
      </div>

      <div className="screen-layout">
        <form
          className="panel screen-form"
          onSubmit={screen}
        >
          <div className="panel-heading">
            <div>
              <h3>Run screening</h3>

              <p>
                Select a job and candidate to analyze.
              </p>
            </div>
          </div>

          <label>Job</label>

          <select
            value={jobId}
            onChange={(e) =>
              setJobId(e.target.value)
            }
          >
            {jobs.length === 0 ? (
              <option value="">
                No jobs available
              </option>
            ) : (
              jobs.map((job) => (
                <option
                  key={job.id}
                  value={job.id}
                >
                  {job.title ||
                    `Job #${job.id}`}
                </option>
              ))
            )}
          </select>

          <label>Candidate</label>

          <select
            value={candidateId}
            onChange={(e) =>
              setCandidateId(
                e.target.value
              )
            }
          >
            {candidates.length === 0 ? (
              <option value="">
                No candidates available
              </option>
            ) : (
              candidates.map(
                (candidate) => (
                  <option
                    key={candidate.id}
                    value={candidate.id}
                  >
                    {candidate.name ||
                      candidate.email ||
                      `Candidate #${candidate.id}`}
                  </option>
                )
              )
            )}
          </select>

          {error && (
            <div className="error-box">
              {error}
            </div>
          )}

          <button
            className="primary-btn full"
            disabled={
              loading ||
              !jobId ||
              !candidateId
            }
          >
            <Sparkles size={17} />

            {loading
              ? "Analyzing..."
              : "Run AI screening"}
          </button>
        </form>

        {result ? (
          <ScreeningResult
            result={result}
          />
        ) : (
          <div className="panel result-placeholder">
            <div className="placeholder-icon">
              <Sparkles size={26} />
            </div>

            <h3>Screening results</h3>

            <p>
              Select a job and candidate to
              see the AI-powered screening
              result.
            </p>
          </div>
        )}
      </div>
    </>
  );
}

function ScreeningResult({
  result,
}) {
  const matched =
    result.matched_skills
      ? result.matched_skills
          .split(",")
          .map((x) => x.trim())
          .filter(Boolean)
      : [];

  const missing =
    result.missing_skills
      ? result.missing_skills
          .split(",")
          .map((x) => x.trim())
          .filter(Boolean)
      : [];

  return (
    <div className="panel screening-result">
      <div className="result-header">
        <div>
          <div className="eyebrow">
            SCREENING COMPLETE
          </div>

          <h2>
            Candidate assessment
          </h2>
        </div>

        <div className="score-circle">
          <strong>
            {result.overall_score}
          </strong>

          <span>/100</span>
        </div>
      </div>

      <div className="recommendation">
        <CheckCircle2 size={17} />
        {result.recommendation}
      </div>

      <div className="score-grid">
        <ScoreMetric
          label="Overall score"
          value={result.overall_score}
        />

        <ScoreMetric
          label="Skill match"
          value={result.skill_score}
        />

        <ScoreMetric
          label="Experience"
          value={
            result.experience_score
          }
        />
      </div>

      <div className="skills-section">
        <h3>Matched skills</h3>

        <div className="skill-list">
          {matched.length > 0 ? (
            matched.map((skill) => (
              <span
                className="skill matched"
                key={skill}
              >
                <CheckCircle2 size={14} />
                {skill}
              </span>
            ))
          ) : (
            <span className="muted">
              No matched skills
            </span>
          )}
        </div>
      </div>

      <div className="skills-section">
        <h3>Missing skills</h3>

        <div className="skill-list">
          {missing.length > 0 ? (
            missing.map((skill) => (
              <span
                className="skill missing"
                key={skill}
              >
                <XCircle size={14} />
                {skill}
              </span>
            ))
          ) : (
            <span className="muted">
              No missing skills
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

function NavItem({
  icon,
  label,
  active,
  onClick,
}) {
  return (
    <button
      className={`nav-item ${
        active ? "active" : ""
      }`}
      onClick={onClick}
    >
      {icon}
      <span>{label}</span>
    </button>
  );
}

function StatCard({
  icon,
  label,
  value,
  small,
}) {
  return (
    <div className="stat-card">
      <div className="stat-icon">
        {icon}
      </div>

      <div>
        <span>{label}</span>

        <strong
          className={
            small
              ? "online-text"
              : ""
          }
        >
          {value}
        </strong>
      </div>
    </div>
  );
}

function WorkflowStep({
  number,
  title,
  text,
}) {
  return (
    <div className="workflow-step">
      <div className="step-number">
        {number}
      </div>

      <div>
        <strong>{title}</strong>

        <p>{text}</p>
      </div>
    </div>
  );
}

function Feature({
  title,
  text,
}) {
  return (
    <div className="feature">
      <div className="feature-check">
        <CheckCircle2 size={16} />
      </div>

      <div>
        <strong>{title}</strong>
        <span>{text}</span>
      </div>
    </div>
  );
}

function ScoreMetric({
  label,
  value,
}) {
  const numericValue =
    Number(value) || 0;

  return (
    <div className="score-metric">
      <span>{label}</span>

      <strong>
        {numericValue}%
      </strong>

      <div className="progress">
        <div
          className="progress-fill"
          style={{
            width: `${Math.min(
              numericValue,
              100
            )}%`,
          }}
        />
      </div>
    </div>
  );
}

function EmptyState({
  icon,
  title,
  text,
}) {
  return (
    <div className="empty-state">
      <div className="empty-icon">
        {icon}
      </div>

      <strong>{title}</strong>

      <span>{text}</span>
    </div>
  );
}

export default App;