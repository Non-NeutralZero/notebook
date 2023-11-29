+++
title = "Hive"
description = ""
tags = [
    "sql",
    "hql",
    "development",
]
date = "2018-04-02"
categories = [
    "Utils",
]
menu = "main"
parent = "tutorials"
+++

## Snippets

```sql
-- set identifiers to none for the query below to work and 
-- set it back to column once it's done
set hive.support.quoted.identifiers = none;
```
## HIVE 3
- BI Code typically use `db.table` - needs to change to `db`.`table`
- Default path : /warehouse/tablespace/external/hive/default.db/test_table

## Resources & Useful Links
[ACID + HIVE](https://cwiki.apache.org/confluence/display/Hive/Hive+Transactions)