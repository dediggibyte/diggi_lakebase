
# diggi_lakebase 
# <img width="164" alt="image" src="https://github.com/user-attachments/assets/dee324eb-9439-4b08-851e-08541d1505a4" />
End-to-end scripts and SQL to **benchmark Databricks Lakebase** against managed PostgreSQL for OLTP + real-time analytics workloads and **Monitor the cost of Lakebase** using AI/BI Dashboards.

---

## 1. What’s inside?

| Path | Purpose |
|------|---------|
| `benchmark/01_Utility.py` | Helper functions (token auth, connection retries, data generators). |
| `benchmark/02_Lakebase_loader.py` | Bulk-loads synthetic or CSV data into Lakebase tables. |
| `benchmark/03_latency_check.py` | Runs pgbench-style throughput/latency tests and streams metrics to stdout. |
| `benchmark/custom_test.sql` | SQL harness for concurrency / branching scenarios. |

---

## 2. Prerequisites

* **Databricks Workspace** with ✨ Lakebase preview enabled.  
* **Unity Catalog** enabled.  
* Python `3.10+` (locally)  
* Databricks CLI with Bundles support installed and configured (`databricks --version` ≥ 0.221).  
* A SQL Warehouse ID with access to `system.billing.*` and `system.access.*` for cost views.  

---

## 3. Benchmark Lakebase

- **Set connection in `benchmark/01_Utility.py`**: Open in a Databricks notebook and set `password` (token or password), `user`, `database_host`, `database_port`, `database_name`.
- **Load data**: Run `benchmark/02_Lakebase_loader.py` to generate and write sample tables:
  - `sc_lakebase_demo.vehicle_ins_idx_big` (~4M rows)
  - `sc_lakebase_demo.customer_orders`
- **Run latency/throughput test**: Run `benchmark/03_latency_check.py`. It installs `pgbench` on the cluster and runs it with `benchmark/custom_test.sql` (mixed UPDATE/SELECT workload). Tune flags inside the notebook or use the equivalent `pgbench` args:

```bash
pgbench -n -h $database_host -p $database_port -U $user \
  -f custom_test.sql \
  -T 180 \
  -c 180 \
  -j 6 \
  $database_name
```

Notes:
- Use a runtime that allows apt-get in `%sh` (DBR 13+ recommended).
- Adjust table names or row counts in `02_Lakebase_loader.py` if needed.

---

## 4. Cost Observability (DABs + AI/BI Dashboard)

This repo includes a Databricks Asset Bundle at `lakebase_cost/lakebase-cost-observability/` that deploys:
- Views over `system.billing` and `system.access` for Lakebase costs
- A Databricks AI/BI dashboard: "Lakebase Cost Overview"

### 4.1 Configure
1) Set environment for CLI:

```bash
export DATABRICKS_HOST="https://<your-workspace>.databricks.net"
export DATABRICKS_TOKEN="<personal-access-token>"
```

2) Edit `lakebase_cost/lakebase-cost-observability/databricks.yml`:
- `variables.warehouse_id`: your SQL Warehouse ID
- `targets.dev.workspace.host`: your workspace URL
- Optionally adjust `variables.catalog` and `variables.schema`

Note: The provided SQL creates views in `databricks_lakebase.lakebase_cost` by default. If you need a different catalog/schema, update the SQL under `src/sql/*` accordingly.

### 4.2 Deploy and materialize views

```bash
cd lakebase_cost/lakebase-cost-observability
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run materialize_lakebase_cost_views -t dev -- --DATABRICKS_WAREHOUSE_ID <WAREHOUSE_ID>
```

This will run `src/run_lsql.ipynb`, executing the SQL in `src/sql/` in order defined by `src/lsql.json`.

### 4.3 Open the dashboard
- In the workspace, search for dashboard named "Lakebase Cost Overview"
- Point it to the configured SQL Warehouse if prompted
- Explore daily and monthly Lakebase cost rollups by workspace and user

---
