# Deliverables for Cursor: ER Diagram, Alembic Migrations, and Versioned JSON Schemas

Below are step-by-step instructions and best practices to hand off to Cursor for establishing your database design, initial migrations, and JSON Schema repository.

---

## 1. Canonical ER Diagram & JSONB Usage Guidelines

### 1.1 Define Core Entities and Relationships  
- **Entities:** Corpus, Document, Chunk, Job, Task  
- **Relationships:**  
  - A **Corpus** has many **Documents**  
  - A **Document** has many **Chunks**  
  - A **Job** processes many **Chunks** (via Tasks)  
  - A **Task** ties one **Job** to one **Chunk** run  

### 1.2 Create the ER Diagram  
1. Choose an ERD tool (pgAdmin4, DBeaver, Lucidchart) and connect to your dev Postgres instance.  
2. Model tables for each entity with primary/foreign keys.  
3. Include `metadata` and `framework_data` as JSONB columns on Document and Chunk tables.  
4. Export the diagram as PNG/SVG and embed it in the repo’s `/docs/ERD` folder.

### 1.3 JSONB Usage Guidelines  
- **Hybrid Relational–Document Model:** Store fixed, frequently queried fields (IDs, timestamps, status) as traditional columns; put variable or extension data in JSONB (`metadata`, `framework_data`) to preserve flexibility[1].  
- **Indexing:** Create GIN indexes on JSONB columns for paths you’ll query often, e.g.  
CREATE INDEX idx_chunk_frameworkON chunk USING gin ((framework_data->'civicVirtue'));

text
- **Performance:** Use JSONB’s binary storage to traverse nested keys without full-document scans, and plan for partitioning large tables by `date` or `corpus_id` as data grows[1].

---

## 2. Initial Alembic Migration Scripts

### 2.1 Set Up Alembic  
1. Install:  
pip install alembic psycopg2-binary

text
2. Initialize:  
alembic init alembic

3. Configure `alembic.ini` with your Postgres URL and update `env.py` to import your SQLAlchemy `Base` metadata.

### 2.2 Generate & Review the First Revision  
1. Create revision:  
alembic revision --autogenerate -m "Initial core tables"
2. In the new script (`alembic/versions/*.py`), ensure tables include:  
- JSONB columns with server_default `'{}'`  
- Proper foreign-key constraints  
3. Adjust types if needed (e.g., `postgresql.JSONB` for metadata).

### 2.3 Apply & Test Migrations  
1. Apply migration:  
alembic upgrade head
2. Verify schema in Postgres and run smoke tests against your “golden set” data.

---

## 3. Versioned JSON Schema Repository

### 3.1 Repository Structure  
schemas/├── core_schema_v1.0.0.json├── cv_extension_v1.0.0.json├── mrp_extension_v1.0.0.json├── ps_extension_v1.0.0.json└── README.md

### 3.2 Semantic Versioning & Publishing  
- **File Naming:** Include version in filename (e.g., `_v1.0.0.json`).  
- **$id Property:** In each schema’s root, set:  
{"$schema": "~[https://json-schema.org/draft/2020-12/schema](https://json-schema.org/draft/2020-12/schema)~","$id": "~[https://your-repo.github.io/schemas/core_schema_v1.0.0.json](https://your-repo.github.io/schemas/core_schema_v1.0.0.json)~",…}
- **Git Tags:** Tag each release in Git (e.g., `git tag v1.0.0` → `git push --tags`).

### 3.3 Migration Scripts  
- **jq/Python Scripts:** For each version bump, provide a script in `schemas/migrations/` that transforms older JSONL records to the new schema version[4].  
- **json-schema-migrate:** Optionally, use `json-schema-migrate` to update schema drafts programmatically[10].  

### 3.4 Documentation  
- In `schemas/README.md`, describe:  
- Versioning policy (SemVer) and `$id` usage.  
- How to run migration scripts.  
- How to reference schemas in data and code.

---

With these artifacts—an ER diagram and guidelines, Alembic migration scripts, and a versioned JSON Schema repo—Cursor will have a clear blueprint to implement a robust, evolvable data layer for Milestone 1 and beyond.

---

#personal/writing/narrativegravity