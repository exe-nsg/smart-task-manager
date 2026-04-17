import { useState, useEffect, useCallback } from "react";
import "./App.css";

const API = "http://localhost:8000";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("medium");
  const [dueDate, setDueDate] = useState("");
  const [dueTime, setDueTime] = useState("");
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);

  useEffect(() => { fetchTasks(); }, []);




  const fetchTasks = async () => {
    try {
      const res = await fetch(`${API}/tasks`);
      const data = await res.json();
      setTasks(data.tasks);
    } catch (err) {
      console.error(err);
    } finally {
      setFetching(false);
    }
  };

  const createTask = async () => {
    if (!title.trim()) return alert("Please enter a task title");
    setLoading(true);
    try {
      const due = dueDate && dueTime ? `${dueDate}T${dueTime}:00` : null;
      const res = await fetch(`${API}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description, priority, due_date: due }),
      });
      const data = await res.json();
      setTasks([data.task, ...tasks]);
      setTitle("");
      setDescription("");
      setPriority("medium");
      setDueDate("");
      setDueTime("");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const deleteTask = async (id) => {
    await fetch(`${API}/tasks/${id}`, { method: "DELETE" });
    setTasks(tasks.filter((t) => t.id !== id));
  };

  const completeTask = async (id) => {
    await fetch(`${API}/tasks/${id}/complete`, { method: "PUT" });
    setTasks(tasks.map((t) => t.id === id ? { ...t, completed: true } : t));
  };

  const scoreColor = (s) => s >= 80 ? "#f43f5e" : s >= 50 ? "#f59e0b" : "#10b981";
  const priorityClass = (score) => score >= 80 ? "high" : score >= 50 ? "medium" : "low";
  const completed = tasks.filter((t) => t.completed).length;
  const pending = tasks.length - completed;

  const formatDueDate = (dateStr) => {
    if (!dateStr) return null;
    const d = new Date(dateStr);
    return d.toLocaleString("en-US", {
      weekday: "short", month: "short", day: "numeric",
      hour: "2-digit", minute: "2-digit"
    });
  };

  const isOverdue = (dateStr) => {
    if (!dateStr) return false;
    return new Date(dateStr) < new Date();
  };

  return (
    <div className="app">

      {/* ── HERO ── */}
      <div className="hero">
        <span className="hero-icon">🧠</span>
        <h1>Smart Task Manager</h1>
        <p>Powered by Groq AI</p>
      </div>

      {/* ── STATS ── */}
      <div className="stats-bar">
        <div className="stat-card">
          <div className="stat-number">{tasks.length}</div>
          <div className="stat-label">Total</div>
        </div>
        <div className="stat-card done">
          <div className="stat-number">{completed}</div>
          <div className="stat-label">Done</div>
        </div>
        <div className="stat-card pending">
          <div className="stat-number">{pending}</div>
          <div className="stat-label">Pending</div>
        </div>
      </div>

      {/* ── FORM ── */}
      <div className="form-card">
        <h2>✏️ Add New Task</h2>
        <input
          className="input"
          placeholder="What do you need to do?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && createTask()}
        />
        <textarea
          className="textarea"
          placeholder="Add more details... (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <select className="select" value={priority} onChange={(e) => setPriority(e.target.value)}>
          <option value="high">🔴 High Priority</option>
          <option value="medium">🟡 Medium Priority</option>
          <option value="low">🟢 Low Priority</option>
        </select>

        {/* Date & Time row */}
        <div className="datetime-row">
          <div className="input-group">
            <label>📅 Due Date</label>
            <input
              type="date"
              className="input"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
            />
          </div>
          <div className="input-group">
            <label>⏰ Due Time</label>
            <input
              type="time"
              className="input"
              value={dueTime}
              onChange={(e) => setDueTime(e.target.value)}
            />
          </div>
        </div>

        <button
          className={`btn-add ${loading ? "loading" : ""}`}
          onClick={createTask}
          disabled={loading}
        >
          {loading ? "⏳ AI is analyzing your task..." : "➕ Add Task"}
        </button>
      </div>

      {/* ── TASK LIST ── */}
      <div className="section-header">
        <span className="section-title">Your Tasks</span>
        <span className="count-badge">{tasks.length}</span>
      </div>

      {fetching && (
        <>
          <div className="skeleton" />
          <div className="skeleton" />
          <div className="skeleton" />
        </>
      )}

      {!fetching && tasks.length === 0 && (
        <div className="empty-state">
          <span className="empty-icon">📋</span>
          <div className="empty-title">No tasks yet</div>
          <div className="empty-desc">Add your first task above and let AI analyze it!</div>
        </div>
      )}

      {tasks.map((task, i) => {
        const ai = task.ai_analysis;
        const color = ai ? scoreColor(ai.priority_score) : "#8b5cf6";
        const pClass = ai ? priorityClass(ai.priority_score) : "";
        const circumference = 2 * Math.PI * 24;
        const filled = ai ? (ai.priority_score / 100) * circumference : 0;
        const overdue = isOverdue(task.due_date) && !task.completed;

        return (
          <div
            key={task.id}
            className={`task-card ${task.completed ? "completed" : pClass}`}
            style={{ animationDelay: `${i * 0.05}s` }}
          >
            {/* Title */}
            <div className="task-top">
              <div className="task-title">{task.title}</div>
              {task.completed && <span className="done-pill">✅ Done</span>}
              {overdue && <span className="overdue-pill">⚠️ Overdue</span>}
            </div>

            {/* Description */}
            {task.description && (
              <div className="task-desc">{task.description}</div>
            )}

            {/* Due date */}
            {task.due_date && (
              <div className={`due-date ${overdue ? "overdue" : ""}`}>
                📅 {formatDueDate(task.due_date)}

              </div>
            )}

            {/* AI Analysis */}
            {ai && (
              <>
                {/* Score ring */}
                <div className="score-row">
                  <div className="score-circle">
                    <svg width="60" height="60" viewBox="0 0 56 56">
                      <circle className="score-circle-bg" cx="28" cy="28" r="24" />
                      <circle
                        className="score-circle-fill"
                        cx="28" cy="28" r="24"
                        stroke={color}
                        strokeDasharray={`${filled} ${circumference}`}
                      />
                    </svg>
                    <div className="score-inside">{ai.priority_score}</div>
                  </div>
                  <div className="score-info">
                    <div className="score-num" style={{ color }}>{ai.priority_score}/100</div>
                    <div className="score-sub">AI Priority Score</div>
                  </div>
                </div>

                {/* Pills */}
                <div className="pills">
                  <span className="pill">⏱ {ai.estimated_time}</span>
                  <span className="pill">📁 {ai.category}</span>
                  <span className="pill">🕐 {ai.best_time}</span>
                  {ai.difficulty_level && <span className="pill">💪 {ai.difficulty_level}</span>}
                  {ai.energy_required && <span className="pill">⚡ {ai.energy_required} Energy</span>}
                  {ai.deadline_sensitivity && <span className="pill">🚨 {ai.deadline_sensitivity}</span>}
                </div>

                {/* Motivation */}
                {ai.motivation && (
                  <div className="motivation-box">
                    <div className="motivation-label">💜 Motivation</div>
                    <div className="motivation-text">{ai.motivation}</div>
                  </div>
                )}

                {/* Suggestion */}
                <div className="suggestion">
                  <div className="suggestion-label">AI Suggestion</div>
                  <div className="suggestion-text">💡 {ai.suggestion}</div>
                </div>

                {/* Steps */}
                {ai.steps && ai.steps.length > 0 && (
                  <div className="steps">
                    <div className="steps-label">Action Steps</div>
                    {ai.steps.map((step, idx) => (
                      <div className="step" key={idx}>
                        <span className="step-num">{idx + 1}</span>
                        <span>{step}</span>
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}

            {/* Buttons */}
            <div className="task-actions">
              {!task.completed && (
                <button className="btn-complete" onClick={() => completeTask(task.id)}>
                  ✅ Complete
                </button>
              )}
              <button className="btn-delete" onClick={() => deleteTask(task.id)}>
                🗑 Delete
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default App;