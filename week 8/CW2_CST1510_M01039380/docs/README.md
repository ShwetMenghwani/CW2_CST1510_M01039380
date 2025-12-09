# Week 8: Data Pipeline & CRUD (SQL) – CST1510 CW2

**Student Name:** Shwet Menghwani  
**Student ID:**   M01039380
**Course:**      CST1510 – Multi-Domain Intelligence Platform

## Project Status: WEEK 8 COMPLETE

Successfully migrated from file-based storage to a full **SQLite database** with secure authentication and complete data pipeline.

### Features Implemented
- User migration from `users.txt` → SQLite with bcrypt hashing
- Four domain tables created:
  - `users`
  - `cyber_incidents`
  - `datasets_metadata`
  - `it_tickets`
- Full **CRUD operations** (Create, Read, Update, Delete) for all domains
- CSV data loading using **pandas**
- 100% **parameterized queries** – no SQL injection risk
- Clean modular structure (`app/data/`, `app/services/`)
- One-command full setup & testing via `main.py`

### Database Schema
```sql
users (id, username, password_hash, role)
cyber_incidents (id, date, incident_type, severity, status, description, reported_by)
datasets_metadata (id, dataset_name, size_mb, format, description, source, created_date)
it_tickets (id, date, issue_type, priority, status, description, assigned_to)