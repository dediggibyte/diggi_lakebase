# diggi_lakebase
This repository is for exploratory purpose on Databricks Lakebase

| **Codespaces** | Press the green **Code ▾** button → **Codespaces** → **Create codespace**. You’ll get a VS Code session in the cloud with Git already configured. | Nice balance of full IDE and zero local installs. |

Once your pull request is merged, the repository’s **default branch** (likely `main`) will show the new README immediately. :contentReference[oaicite:0]{index=0}

---

## 2 — **Recommended README content (drop-in template)**

Paste the snippet below into `README.md` (replace the ▢ placeholders). Feel free to reorder or trim sections that aren’t relevant.

```markdown
# diggi_lakebase 🦾📊

> End-to-end scripts and SQL to **benchmark Databricks Lakebase** against managed PostgreSQL for OLTP + real-time analytics workloads.

---

## 1. What’s inside?

| Path | Purpose |
|------|---------|
| `01_Utility.py` | Helper functions (token auth, connection retries, data generators). |
| `02_Lakebase_loader.py` | Bulk-loads synthetic or CSV data into Lakebase tables. |
| `03_latency_check.py` | Runs pgbench-style throughput/latency tests and streams metrics to stdout. |
| `custom_test.sql` | SQL harness for concurrency / branching scenarios. |

---

## 2. Prerequisites

* **Databricks Workspace** with ✨ Lakebase preview enabled.  
* **Unity Catalog** enabled.  
* Python `3.10+` (locally)  

