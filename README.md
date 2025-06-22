
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
