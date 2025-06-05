# Security Guidelines for Cursor

## 1. Secure Development Environment  
- **Environment Isolation:**  
  Run services (API, Redis, Postgres, workers) in Docker containers to isolate dependencies and reduce host attack surface[1].  
- **Access Control:**  
  Use SSH keys (not passwords) for any remote access and enforce least-privilege permissions on local filesystem and Docker sockets[1].  
- **Multi-Factor Authentication:**  
  If code or servers ever move off your laptop, require MFA on Git hosting and container registries[1].  
- **Regular Updates:**  
  Keep OS, Docker Engine, base images, and dependencies up-to-date; integrate Dependabot or GitHub’s security alerts to catch vulnerabilities early[1][5].  

## 2. Secure Coding Practices  
- **Linters & Static Analysis:**  
  Integrate security-focused linters (e.g., Bandit for Python, ESLint security plugins) in CI to detect common issues automatically[1][5].  
- **Input Validation & Sanitization:**  
  Validate all API inputs against JSON Schemas and sanitize any user-supplied content to prevent injection attacks[3].  
- **Peer Reviews & Automated Tests:**  
  Require pull-request reviews for all code changes and include security tests (unit and integration) in your CI pipeline[5].  

## 3. API Security  
- **Token-Based Authentication:**  
  Protect all endpoints with bearer tokens or OAuth 2.0 access tokens issued by a central auth service (even if stubbed locally)[2].  
- **Rate Limiting & Throttling:**  
  Implement request throttling at the API layer (or via a local API gateway) to prevent abuse and runaway costs[3].  
- **Transport Security (TLS):**  
  Use HTTPS for all internal and external communication—even locally via self-signed certificates—to prevent credential leakage[3].  
- **API Gateway (Future-Proofing):**  
  Design your APIs so they can sit behind a gateway (e.g., Kong, Ambassador) that enforces logging, IP allow-lists, and WAF rules when you go to cloud[2][3].  

## 4. Secrets Management  
- **Environment Variables:**  
  Store API keys, database credentials, and Hugging Face tokens in environment variables or a local secrets file excluded from version control (`.env` + `.gitignore`)[1].  
- **Secret Encryption:**  
  For any stored secrets (e.g., in CI), use a vault (HashiCorp Vault, AWS Secrets Manager) or encrypted GitHub Secrets[1].  

## 5. Data Protection & Backup  
- **Encrypted Storage:**  
  Enable native PostgreSQL encryption-at-rest if available, and consider filesystem encryption on your laptop for sensitive corpora[4].  
- **Regular Backups:**  
  Schedule automated backups of Postgres and Redis snapshots; store backups securely and test restores periodically[4].  

## 6. Monitoring, Logging & Alerts  
- **Structured Logging:**  
  Emit JSON logs for ingestion, tasks, and API calls without sensitive data; configure log rotation to prevent disk exhaustion[2].  
- **Health Endpoint:**  
  Expose `/api/health` that checks database connectivity, Redis, and Hugging Face API reachability; integrate basic alerting (e.g., email or Slack) on failures[3].  

## 7. Dependency & Supply-Chain Security  
- **Lockfile Management:**  
  Commit `Pipfile.lock` or `requirements.txt` with pinned versions; periodically rebuild to incorporate security patches.  
- **Supply-Chain Controls:**  
  Vet any third-party libraries for known vulnerabilities; avoid pulling in large dependency trees unless necessary[4].  

---

#personal/writing/narrativegravity