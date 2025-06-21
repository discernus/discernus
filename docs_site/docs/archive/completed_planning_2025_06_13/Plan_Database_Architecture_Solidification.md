# Plan: Database Architecture Solidification (v2.1)

## 🎯 Objective
Ensure the PostgreSQL database architecture is robust, optimized, and fully aligned with the research requirements for iterative experimentation, provenance tracking, and reliable data storage. This includes verifying schema integrity, optimizing queries, and establishing clear data management protocols.

## 🚀 Key Tasks

### 1. **Schema Review and Optimization**
- **1.1. Comprehensive Schema Audit:** Review all existing tables (`experiments`, `runs`, `configurations`, `users`, etc.) for logical consistency, correct data types, and appropriate indexing.
    - *Action:* Verify `varchar` limits are sufficient for new LLM model names (e.g., as addressed in `CURRENT_STATE_REFERENCE.md`).
    - *Action:* Confirm all foreign key relationships and constraints are correctly defined and enforced.
- **1.2. Performance Analysis:** Identify any potential bottlenecks in data retrieval or storage, particularly for large-scale analysis results.
    - *Action:* Run `EXPLAIN ANALYZE` on common API queries (e.g., `/api/analysis-results`) to identify slow queries.
    - *Action:* Add or optimize database indexes based on query patterns for improved performance.
- **1.3. Data Model Alignment:** Ensure database models (`src/narrative_gravity/models/`) accurately reflect the requirements for hierarchical results, provenance tracking (prompt versions, framework versions, LLM models), and comparative analysis as outlined in `Gravity Wells 2.1 Workstream 1 User Stories.md`.

### 2. **Migration Management (`Alembic`)**
- **2.1. Verify Migration History:** Confirm that all necessary Alembic migrations have been applied and that the database schema is up-to-date with the latest code.
    - *Action:* Run `alembic history` and `alembic current` to verify the state.
    - *Action:* Document any manual schema adjustments that may have been made outside of Alembic and integrate them into a migration if appropriate.
- **2.2. Develop New Migrations (if needed):** Create new migration scripts for any identified schema improvements or additions.
    - *Action:* Ensure migrations are idempotent and reversible.
    - *Action:* Test new migrations in a development environment.

### 3. **Data Integrity and Persistence**
- **3.1. Robust Data Saving:** Confirm that all analysis results, experiment configurations, and metadata are reliably persisted to PostgreSQL without errors.
    - *Action:* Conduct stress tests by saving a large volume of simulated analysis results.
    - *Action:* Monitor application logs for any database-related errors during data writes.
- **3.2. Data Retrieval Verification:** Ensure that data can be consistently and correctly retrieved by the API and frontend, especially for complex queries involving joined tables.
    - *Action:* Develop specific integration tests for data retrieval scenarios.
    - *Action:* Verify the integrity of historical data.

### 4. **Connection and Health Monitoring**
- **4.1. Enhance `check_database.py`:** Add more comprehensive checks to the existing database health script.
    - *Action:* Include checks for specific table existence or basic data counts.
    - *Action:* Add error handling and user-friendly messages for common connection issues.
- **4.2. Environment Variable Management:** Ensure `DATABASE_URL` and other database-related environment variables are correctly configured and documented in `env.example`.

## 🛠️ Tools & Commands
- `python check_database.py`
- `alembic revision --autogenerate -m "<description>"`
- `alembic upgrade head`
- `alembic downgrade -1`
- `psql` (for direct database inspection)
- `EXPLAIN ANALYZE` (SQL command for query optimization)

## ✅ Validation Criteria
- [ ] Database connection is consistently stable.
- [ ] All data models are accurately reflected in the PostgreSQL schema.
- [ ] Data persistence for experiments, runs, and configurations is 100% reliable.
- [ ] Key data retrieval queries are optimized and perform efficiently.
- [ ] All Alembic migrations are up-to-date and apply without errors.
- [ ] `check_database.py` provides clear and accurate status of the database. 