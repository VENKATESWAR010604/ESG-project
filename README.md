# Breathe ESG Review Dashboard

A full-stack ESG data ingestion and review application built for the Breathe ESG assignment.

The app ingests activity data from SAP fuel/procurement files, utility electricity files, and travel records. It normalizes the data into one review table where users can approve, reject, delete, and audit ESG activity rows.

---

## Tech Stack

### Frontend
- React
- Vite
- Axios
- CSS

### Backend
- Django
- Django REST Framework
- SQLite for local development

---

## Features

- Ingest SAP fuel/procurement data
- Ingest utility electricity data
- Ingest travel data
- Normalize all sources into one common activity row model
- Categorize records into Scope 1, Scope 2, and Scope 3
- Mark invalid rows as FAILED
- Mark unusual rows as SUSPICIOUS
- Approve or reject review rows
- Audit log for reviewer decisions
- Dashboard summary cards
- Filter rows by source and status
- Responsive frontend layout

---

## Project Structure

```text
breatheESG/
├── backend/
│   ├── ingestion/
│   ├── sample_data/
│   ├── db.sqlite3
│   └── manage.py
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── README.md
├── MODEL.md
├── DECISIONS.md
├── TRADEOFFS.md
└── SOURCES.md