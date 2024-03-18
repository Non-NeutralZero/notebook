+++
title = "Multi-module build based on sbt"
description = ""
tags = [
    "scala",
    "templates",
    "development",
]
date = "2024-03-15"
categories = [
    "Development",
    "Documentation",
]
menu = "main"
parent = "tutorials"
+++

```scala
import sbt.{Compile, Test, *}
import Keys.{baseDirectory, libraryDependencies, *}

// sbt.version = 1.6.2
ThisBuild / trackInternalDependencies := TrackLevel.TrackIfMissing

lazy val welcome = taskKey[Unit]("welcome")

val sparkVersion = "2.4.0-cdh6.2.1"
val hiveVersion = "2.1.1-cdh6.2.1"

lazy val commonSettings = Seq(
  //organization := "com.nnz",
  version := "0.1.0-SNAPSHOT",
  welcome := { println("Welcome !")},
  scalaVersion := "2.11.12",
  javacOptions ++= Seq("-source", "15.0.10", "-target", "15.0.10"),
  libraryDependencies ++= sparkDependencies,
  resolvers ++= Seq("Cloudera Versions" at "https://repository.cloudera.com/artifactory/cloudera-repos/",
  )
)

lazy val root = (project in file("."))
  .settings(
    name := "multimodule-project",
    commonSettings,
    update / aggregate :=  true,
  )
  .aggregate(warehouse, ingestion, processing)

lazy val warehouse = (project in file("warehouse"))
  .settings(
    name := "warehouse",
    commonSettings,
    Compile / scalaSource := baseDirectory.value /"." / "src" / "main" / "scala",
    Test / scalaSource := baseDirectory.value  /"." / "src" / "test" / "scala",
  )

lazy val ingestion = (project in file("ingestion"))
  .dependsOn(warehouse)
  .settings(
    name := "ingestion",
    commonSettings,
    Compile / scalaSource := baseDirectory.value /"." / "src" / "main" / "scala",
    Test / scalaSource := baseDirectory.value  /"." / "src" / "test" / "scala",
  )

lazy val processing = (project in file("processing"))
  .dependsOn(warehouse, ingestion)
  .settings(
    name := "processing",
    commonSettings,
    Compile / scalaSource := baseDirectory.value /"." / "src" / "main" / "scala",
    Test / scalaSource := baseDirectory.value  /"." / "src" / "test" / "scala",
  )

/**
 * Spark Dependencies
 */
val sparkCore = "org.apache.spark" %% "spark-core" % sparkVersion
val sparkSQL = "org.apache.spark" %% "spark-sql" % sparkVersion
val sparkHive = "org.apache.spark" %% "spark-hive" %  sparkVersion

lazy val sparkDependencies = Seq(sparkCore, sparkSQL, sparkHive)
```
