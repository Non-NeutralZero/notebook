+++
title = "Databricks and OOP, do they match ?"
description = "Exploring whether Object-Oriented Programming (OOP) fits well with Databricks and Spark-based workflows."
tags = [
    "databricks",
    "spark",
    "oop",
    "software-engineering"
]
date = "2025-09-02"
categories = [
    "Development",
    "Architecture",
]
menu = "main"
parent = "notebook"
+++

## Context

Databricks and Apache Spark are often used in data engineering, data science, and machine learning workflows. Their APIs are designed around **distributed data processing** (RDDs, DataFrames, Datasets). The question arises: *does Object-Oriented Programming (OOP) fit into this paradigm, or do we need a different style?*

---

## Databricks Programming Model vs OOP

- **Spark API**: functional and declarative. You express transformations (`map`, `filter`, `select`) on immutable distributed datasets.  
- **OOP style**: encapsulates data + behaviour inside classes, often with mutable state.

### Where They Match
- **Encapsulation of business logic**: Wrapping Spark transformations inside reusable classes (e.g., `DataCleaner`, `FeatureEngineer`) helps modularize pipelines.
- **Abstractions for teams**: Teams can expose high-level methods (`.transform(df)`) instead of low-level Spark calls.
- **Testing & reusability**: OOP structures allow dependency injection, mock data, and unit testing.

### Where They Clash
- **Statefulness**: Spark’s lazy evaluation and immutable DataFrames do not align with mutable OOP state.
- **Serialization**: Classes with methods that capture external state may not serialize well when Spark ships code to executors.
- **Functional preference**: Many Spark best practices push towards functional patterns (pure functions, stateless transformations).

Note on statefulness: In *Learning Spark*, Holden Karau makes distinction between stateless and stateful processing and emphazizes it. Stateless transformations are preferred, but spark also provides patterns for stateful processing, particularly in streaming contexts. e.g., `updateStateByKey`, windowing, watermarking, and event-time state management.

---

## Practical Patterns

1. **Functional Core, OOP Shell**  
Model the pipeline's internal logic with pure, side-effect-free functions; wrap them in OOP constructs for configuration and orchestration.

   Use classes to organize pipelines, but keep transformations as pure functions.  
   ```python
   class ETLPipeline:
       def __init__(self, spark):
           self.spark = spark
       
       def transform(self, df):
           return (
               df.filter(df.value > 0)
                 .withColumn("scaled", df.value * 100)
           )
   ```
2. **Implicit Ops for Cleaner APIs**
```scala
   object dfops {
     implicit final class FeatureOps(private val df: DataFrame) extends AnyVal {
       def countsWithinMilestones(eventTs: String, baseTs: String, key: String,
                                  pivot: String, months: Seq[Int]): DataFrame = {
         // return new DataFrame via Spark SQL functions
         df
       }
     }
   }

   import dfops._
   val out = df.countsWithinMilestones("timestamp", "basedt", "id_client", "pivot", Seq(1,3,6))
   ```
Expose composable, stateless APIs. for example see design in design in the [spark-feature-engineering-toolkit](https://github.com/Non-NeutralZero/spark-feature-engineering-toolkit)

3. **Testing with Spark‑Testing Base**

   ```scala
   import com.holdenkarau.spark.testing.DataFrameSuiteBase
   import org.scalatest.funsuite.AnyFunSuite

   final class FeatureOpsTest extends AnyFunSuite with DataFrameSuiteBase {
     test("countsWithinMilestones yields expected columns") {
       import spark.implicits._
       val df = Seq(("A", "2019-01-01T00:00:00", "MAROC", "retrait_gab", 1500.0))
         .toDF("id_client","timestamp","lieu","type","montant")
       import dfops._
       val out = df.countsWithinMilestones("timestamp", "basedt", "id_client", "pivot", Seq(1,3,6))
       assert(out.columns.exists(_.startsWith("nb_")))
     }
   }
   ```

## TLDR

- Use **OOP for orchestration and API shape** (configuration, sequencing, discoverability).  
- Keep **transformations functional & stateless** (pure functions over `DataFrame`s / `Dataset`s).  
- For **streaming state**, rely on Spark’s state APIs (`mapGroupsWithState`/`flatMapGroupsWithState`, `transformWithState`) instead of mutable class fields.


## References

- Holden Karau et al., Learning Spark, 2nd Edition (O’Reilly, 2020). Chapters on DataFrames and Structured Streaming.

- Holden Karau & Andy Konwinski et al., Spark: The Definitive Guide (O’Reilly, 2018). See discussion of event-time, stateful vs stateless operations.

- [spark-feature-engineering-toolkit](https://github.com/Non-NeutralZero/spark-feature-engineering-toolkit) – Example APIs for composable, stateless feature engineering.

- com.holdenkarau/spark-testing-base – Library for testing Spark applications.