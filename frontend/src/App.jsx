import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

function App() {
  const [summary, setSummary] = useState(null);
  const [rows, setRows] = useState([]);
  const [logs, setLogs] = useState([]);
  const [status, setStatus] = useState("");
  const [source, setSource] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [summaryRes, logsRes, rowsRes] = await Promise.all([
        axios.get(`${API}/review/summary/`),
        axios.get(`${API}/audit/logs/`),
        axios.get(`${API}/review/rows/`, {
          params: { status: status || undefined, source: source || undefined },
        }),
      ]);
      setSummary(summaryRes.data);
      setLogs(logsRes.data);
      setRows(rowsRes.data);
    } catch (error) {
      alert("Backend not running or API error");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [status, source]);

  const approveRow = async (id) => {
    await axios.post(`${API}/review/rows/${id}/approve/`);
    fetchData();
  };

  const rejectRow = async (id) => {
    await axios.post(`${API}/review/rows/${id}/reject/`);
    fetchData();
  };

  const deleteRow = async (id) => {
    if (!confirm("Are you sure you want to delete this row?")) return;
    await axios.delete(`${API}/review/rows/${id}/delete/`);
    fetchData();
  };

  const ingestData = async (type) => {
    await axios.post(`${API}/ingest/${type}/`);
    fetchData();
  };

  const cards = [
    ["Total Rows", summary?.total_rows, "total"],
    ["Pending", summary?.pending_rows, "pending"],
    ["Failed", summary?.failed_rows, "failed"],
    ["Suspicious", summary?.suspicious_rows, "suspicious"],
    ["Approved", summary?.approved_rows, "approved"],
    ["Rejected", summary?.rejected_rows, "rejected"],
  ];

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">
          <div className="logo">B</div>
          <div>
            <h2>Breathe ESG</h2>
            <p>Carbon Review</p>
          </div>
        </div>

        <nav>
          <a href="#dashboard" className="active">Dashboard</a>
          <a href="#ingestion">Data Ingestion</a>
          <a href="#review">Review Rows</a>
          <a href="#audit">Audit Logs</a>
        </nav>

        <div className="sidebar-footer">
          <p>wait for 10sec</p>
          <strong>Live API Connected</strong>
        </div>
      </aside>

      <main className="main">
        <section id="dashboard" className="topbar">
          <div>
            <p className="eyebrow">ESG Data Quality System</p>
            <h1>Review Dashboard</h1>
            <p>Monitor emissions data, approve records, reject suspicious rows, and track audit history.</p>
          </div>

          <button className="refresh" onClick={fetchData}>
            {loading ? "Loading..." : "Refresh"}
          </button>
        </section>

        {summary && (
          <section className="cards">
            {cards.map(([title, value, type]) => (
              <div className={`card ${type}`} key={title}>
                <p>{title}</p>
                <h2>{value ?? 0}</h2>
              </div>
            ))}
          </section>
        )}

        <section id="ingestion" className="panel">
          <div className="panel-header">
            <div>
              <h2>Data Ingestion</h2>
              <p>Import data from SAP, utility bills, and travel systems.</p>
            </div>
          </div>

          <div className="ingest-buttons">
            <button onClick={() => ingestData("sap")}>Ingest SAP</button>
            <button onClick={() => ingestData("utility")}>Ingest Utility</button>
            <button onClick={() => ingestData("travel")}>Ingest Travel</button>
          </div>
        </section>

        <section id="review" className="panel">
          <div className="panel-header">
            <div>
              <h2>Review Rows</h2>
              <p>Filter and review normalized ESG activity rows.</p>
            </div>
          </div>

          <div className="filters">
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
              <option value="">All Status</option>
              <option value="PENDING">Pending</option>
              <option value="FAILED">Failed</option>
              <option value="SUSPICIOUS">Suspicious</option>
              <option value="APPROVED">Approved</option>
              <option value="REJECTED">Rejected</option>
            </select>

            <select value={source} onChange={(e) => setSource(e.target.value)}>
              <option value="">All Sources</option>
              <option value="SAP">SAP</option>
              <option value="UTILITY">Utility</option>
              <option value="TRAVEL">Travel</option>
            </select>

            <button className="clear" onClick={() => { setStatus(""); setSource(""); }}>
              Clear Filters
            </button>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Source</th>
                  <th>Scope</th>
                  <th>Activity</th>
                  <th>Quantity</th>
                  <th>Unit</th>
                  <th>Status</th>
                  <th>Reason</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {rows.map((row) => (
                  <tr key={row.id}>
                    <td>#{row.id}</td>
                    <td>{row.source_type}</td>
                    <td>{row.scope}</td>
                    <td>{row.activity_type}</td>
                    <td>{row.quantity}</td>
                    <td>{row.unit}</td>
                    <td>
                      <span className={`badge ${row.status.toLowerCase()}`}>
                        {row.status}
                      </span>
                    </td>
                    <td>{row.error_reason || row.suspicious_reason || "-"}</td>
                    <td className="actions">
                      {row.status !== "APPROVED" &&
                        row.status !== "REJECTED" &&
                        row.status !== "FAILED" && (
                          <>
                            <button className="approve" onClick={() => approveRow(row.id)}>Approve</button>
                            <button className="reject" onClick={() => rejectRow(row.id)}>Reject</button>
                          </>
                        )}
                      <button className="delete" onClick={() => deleteRow(row.id)}>Delete</button>
                    </td>
                  </tr>
                ))}

                {rows.length === 0 && (
                  <tr>
                    <td colSpan="9" className="empty">No rows found</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        <section id="audit" className="panel">
          <div className="panel-header">
            <div>
              <h2>Audit Logs</h2>
              <p>Track every approval, rejection, deletion, and ingestion action.</p>
            </div>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Log ID</th>
                  <th>Row ID</th>
                  <th>Action</th>
                  <th>Note</th>
                  <th>Created At</th>
                </tr>
              </thead>

              <tbody>
                {logs.map((log) => (
                  <tr key={log.id}>
                    <td>#{log.id}</td>
                    <td>{log.row_id}</td>
                    <td><span className="log-action">{log.action}</span></td>
                    <td>{log.note}</td>
                    <td>{new Date(log.created_at).toLocaleString()}</td>
                  </tr>
                ))}

                {logs.length === 0 && (
                  <tr>
                    <td colSpan="5" className="empty">No audit logs found</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
