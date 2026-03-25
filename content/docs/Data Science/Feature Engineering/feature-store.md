---
bookToc: false
---
version 19-08-2024

## Feature Store as a System

- follows a logical flow
- seperates concerns functionally
- builds modular-ily

{{< figure src="/notebook/images/docs/datascience/feature-store/feature-store-2024-08-24.svg" >}}

 
## Pipeline and code break-down
### Data Selection and UC-specific processing

We start by filtering a reference table based on specific conditions aligned with the requirements of the use case. This creates a use case table on which we select and process pivot columns.

{{< hint info >}}
   **Note:** This should happen in the processing and modeling modules.
   {{< /hint >}}

### Pivot transformations and Data federation
We select specific columns in order to create transitional tables with the desired pivot columns.

We combine all transitional tables using union operations to create a single base table on which the features calculations will occur.

{{< hint info >}}
   **Note:** This base table must have the structure: clientId, pivotCol, valueCol, and eventDateCol.
   {{< /hint >}}

### Features generation
The code defines functions for generating features with different parameters.
The developer chooses which generator or generators to use and applies the generator on the previously created base table (the one created in phase 2.3)


### Memory management
Usage of memory management operations will be necessary. The developer must keep in mind the necessity of optimizing memory usage, especially for large datasets.

## Pipeline and code best practices
### Naming conventions and Nomenclatures
- Variable names are descriptive
- Adhere to Scala conventions as much as possible

### Keep the code modular
- Externalize configurations to make the code more flexible and easier to maintain
- Refactor duplicated codes
- Create specific objects, when needed, to federate segments of operations and functions

### Keep the code readable
- Add inline comments, if necessary, explaining the purpose of each major operation to improve readability
- Add scala documentation to explain the purposes of functions, their usage and requirements
- Adhere to naming conventions

### Error handling and Unit testing
- Consider adding try-catch blocks or other error handling mechanisms, especially for operations that might fail (like reading from or writing to external sources)
- Unit test operations and transformations that are key to the success of the pipeline

