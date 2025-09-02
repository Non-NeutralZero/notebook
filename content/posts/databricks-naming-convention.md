+++
title = "Databricks Naming Conventions"
description = "Concise guidelines for organizing and naming Databricks resources"
tags = ["databricks","best-practices","naming","data-engineering","environment"]
date = "2025-09-02"
categories = ["Development","Data Platforms"]
menu = "main"
parent = "tutorials"
+++

## Introduction

Consistent naming across **env (dev, test, prod)**, **layers (bronze/silver/gold)**, and **domains** is critical in Databricks. It prevents confusion, enforces governance, and supports automation with Unity Catalog and Delta Lake.

---

## General Best Practices

* Separate dev / test / prod workspaces.
* Apply RBAC + Unity Catalog.
* Use modular notebooks; reuse with `%run`.
* Version control all code.
* Prefer job clusters; auto-terminate.
* Vacuum Delta tables; use optimize + z-order.
* Allow schema evolution only when intentional.

---

## Environment‑Aware Medallion Naming

Unity Catalog is the governance backbone. Inconsistent names break access policies and automation. Use env prefixes, clear domains, and snake\_case ([Unity Catalog docs](https://learn.microsoft.com/azure/databricks/data-governance/unity-catalog/) .

Pattern:

```
<env>_<domain>
```

Examples: `prod_sales`, `dev_marketing`, `test_finance`

---

## Layer‑Specific Schemas

Pattern:

```
<env>_<domain>.<layer>
```

Examples: `prod_sales.bronze`, `prod_sales.silver`, `prod_sales.gold`

---

## Table Naming Within Layers

Use snake\_case, descriptive names.

```
bronze.transactions_raw
silver.customer_validated
gold.sales_monthly
```

Full name example: `prod_sales.bronze.transactions_raw`

---

## File Storage Structure

Mirror env/layer/domain/table in paths.

```
/mnt/data/<env>/<layer>/<domain>/<table>/
```

Example: `/mnt/data/prod/bronze/sales/transactions/`

---

## Summary Table

| Level          | Pattern                                     | Example                               |
| -------------- | ------------------------------------------- | ------------------------------------- |
| Catalog        | `<env>_<domain>`                            | `dev_hr`, `prod_sales`                |
| Schema / Layer | `<catalog>.<layer>`                         | `test_finance.bronze`                 |
| Table Name     | snake\_case                                 | `silver.employee_cleaned`             |
| Full Name      | `<catalog>.<layer>.<table>`                 | `prod_sales.gold.monthly_rev`         |
| Storage Path   | `/mnt/data/<env>/<layer>/<domain>/<table>/` | `/mnt/data/dev/bronze/marketing/ads/` |

---

## Good vs Bad Examples

### Workspaces

* **Good**: `dev`, `test`, `prod` separated (pre-prod when maturity allows).
* **Bad**: mixed single workspace.

### Clusters

* **Good**: job clusters with auto-termination.
* **Bad**: idle interactive cluster.

### Schemas / Layers

* **Good**: `prod_sales.bronze`.
* **Bad**: `bronze1`, `myschema`.

### Tables

* **Good**: `silver.customer_validated`.
* **Bad**: `CustomerData`, `table1`.

### Storage Paths

* **Good**: `/mnt/data/prod/gold/finance/revenue_summary/`.
* **Bad**: `/mnt/data/finaltables/finance2024/`.

---

## Community Discussions

| Link                                                                                                                                                                                        | Post                                      | Date     | Latest Reply |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- | -------- | ------------ |
| [Reddit: r/databricks – Naming standards](https://www.reddit.com/r/databricks/comments/182o6us/naming_standards_for_three_level_name_space/?utm_source=chatgpt.com)                         | Confusion scaling naming                  | Dec 2023 | Jan 2024     |
| [Reddit: r/dataengineering – Unity Catalog naming](https://www.reddit.com/r/dataengineering/comments/17pvnt2/unity_catalog_databricks_naming_convention_best/?utm_source=chatgpt.com)       | Environment "grown wild"                  | Nov 2023 | Dec 2023     |
| [Reddit: r/dataengineering – Organizing Unity Catalog](https://www.reddit.com/r/dataengineering/comments/1fkws1g/how_are_teams_organizing_databricks_unity_catalog/?utm_source=chatgpt.com) | Catalog-first vs domain-first             | Aug 2024 | Aug 2024     |
| [Stack Overflow – Catalog vs Database](https://stackoverflow.com/questions/78149033/rationale-for-databricks-naming-catalog-and-database-not-database-and-sch?utm_source=chatgpt.com)       | Terminology confusion                     | Feb 2024 | Feb 2024     |
| [Medium – Unity Catalog Principles](https://medium.com/%40anil.jain.baba/databricks-unity-catalog-guiding-principles-2c08cb9923a6?utm_source=chatgpt.com)                                   | Governance risks from inconsistency       | Sep 2023 | Sep 2023     |
| [Medium – Best Practices](https://medium.com/%40valentin.loghin/databricks-best-practices-and-naming-conventions-105013ec31c9?utm_source=chatgpt.com)                                       | Domain separation pitfalls                | Oct 2023 | Oct 2023     |
| [Medium – Ultimate Guide](https://www.carlosacchi.cloud/the-ultimate-guide-to-databricks-naming-conventions-for-a-scalable-data-lakehouse-9ff816b5f483?utm_source=chatgpt.com)              | Confusion when diverging from snake\_case | Jul 2024 | Jul 2024     |

---

## References

**Official Docs**

* [Databricks Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/)
* [Azure Databricks naming best practices](https://learn.microsoft.com/en-us/azure/databricks/best-practices/naming-conventions)
* [Databricks Medallion Architecture](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion)
* [Azure Q\&A – Organizing multiple source systems](https://learn.microsoft.com/en-us/answers/questions/5526633/best-practice-for-organizing-multiple-source-syste?utm_source=chatgpt.com)

**Community & Practitioner Insights**

* [carlosacchi.cloud – Ultimate Guide](https://www.carlosacchi.cloud/the-ultimate-guide-to-databricks-naming-conventions-for-a-scalable-data-lakehouse-9ff816b5f483?utm_source=chatgpt.com)
* [medium.com – Valentin Loghin](https://medium.com/%40valentin.loghin/databricks-best-practices-and-naming-conventions-105013ec31c9?utm_source=chatgpt.com)
* [reddit.com – Naming standards discussion](https://www.reddit.com/r/databricks/comments/182o6us/naming_standards_for_three_level_name_space/?utm_source=chatgpt.com)
