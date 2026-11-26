---
name: sql-style
description: "Write, edit, or review .sql and SQL migrations using house SQL style unless another guide is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: sql
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# SQL style (house)

Our blend of the best SQL guides, in our own words. Every rule in the full guide names its source.

Scope: PostgreSQL 18 application queries, schema definitions, and migrations; SQLFluff 4.5.0 with the PostgreSQL dialect. Plain SQL is the baseline; dbt/Jinja and procedural function bodies need separate integration. The reference client is PostgreSQL 18.6; a consuming repository pins its server patch release.

If the project declares older versions or its own formatter/linter settings, follow the project and say so.

## Quick rules

- MUST use `CREATE INDEX CONCURRENTLY` and `DROP INDEX CONCURRENTLY` outside transaction blocks on existing populated tables; document an alternative lock plan for operations or table kinds that cannot use them. Why: ordinary index DDL can block live traffic. [SQLFLUFF] [PG-CREATEINDEX] [PG-DROPINDEX]
- MUST use unquoted lowercase snake_case for new schema identifiers and avoid keyword names. Why: PostgreSQL folds unquoted names to lowercase and quoted mixed case creates fragile references. [PG-PITFALLS] [GITLAB-SQL]
- PREFER full relation names or descriptive aliases of at least four characters. Why: readable references preserve the query's domain meaning. [GITLAB-SQL] [SQLFLUFF]
- MUST use explicit AS for every table or column alias. Why: alias declarations remain distinct from expressions and relation names. [HOLYWELL-SQL] [GITLAB-SQL] [SQLFLUFF]
- MUST qualify column references when a query uses multiple relations, including correlated outer references. Why: schema additions must not make a reference ambiguous. [GITLAB-SQL] [SQLFLUFF]
- MUST name computed result columns and enumerate columns at application, view, and export boundaries. Why: consumers need a stable output shape and meaningful field names. [HOLYWELL-SQL] [SQLFLUFF]
- MUST use explicit JOIN syntax and join types; use CROSS JOIN only for an intentional Cartesian product. Why: the relationship and row multiplication remain visible. [GITLAB-SQL] [SQLFLUFF]
- MUST use named references or expressions instead of numeric positions in GROUP BY and ORDER BY. Why: editing the SELECT list must not silently change grouping or sorting. [SQLFLUFF]
- MUST store instants as TIMESTAMPTZ; reserve TIMESTAMP WITHOUT TIME ZONE for deliberate wall-clock values. Why: an unzoned timestamp cannot identify a moment across time zones. [PG-PITFALLS]
- MUST use half-open timestamp windows, value >= start AND value < end, for adjacent periods. Why: inclusive upper bounds double-count boundary events. [PG-PITFALLS]
- PREFER TEXT for PostgreSQL strings, using length or format constraints only for actual domain limits. Why: CHAR padding and arbitrary VARCHAR limits add unwanted behavior. [PG-PITFALLS]
- MUST represent exact monetary amounts with NUMERIC and an explicit currency contract, using a currency column when currencies vary. Why: floating-point approximation and MONEY's locale assumptions lose required meaning. [PG-PITFALLS] [HOLYWELL-SQL]
- PREFER GENERATED ALWAYS AS IDENTITY for new generated integer keys, with PRIMARY KEY or UNIQUE as appropriate. Why: identity manages generation but uniqueness still needs a constraint. [PG-PITFALLS] [PG-CONSTRAINTS]
- MUST enforce relational invariants with primary/unique keys, foreign keys, NOT NULL, and CHECK as appropriate; CHECK alone does not reject NULL. Why: every writer must preserve the same valid database states. [PG-CONSTRAINTS]
- MUST test nullness with IS NULL or IS NOT NULL and choose COALESCE only when the fallback has domain meaning. Why: NULL comparisons and indiscriminate defaults can hide unknown data. [SQLFLUFF] [PG-CONSTRAINTS]
- PREFER correlated NOT EXISTS for subquery exclusions, explicitly deciding how nullable outer keys behave. Why: a NULL in a NOT IN result can suppress every candidate row. [PG-PITFALLS]
- PREFER named CTEs for independent query stages while retaining subqueries needed for correlation or LATERAL semantics. Why: logical stages should be readable without changing their dependencies. [GITLAB-SQL] [PG-WITH]
- MUST choose UNION ALL or UNION DISTINCT explicitly and preserve positional output contracts. Why: duplicate elimination and column position affect the result's meaning. [GITLAB-SQL] [SQLFLUFF]
- MUST give paginated or limited application results a deterministic ORDER BY with a unique tie-breaker. Why: tied or unordered rows do not define a repeatable subset. [SQLFLUFF]
- MUST wrap related writes that must succeed together in one transaction and roll back a failed transaction before reuse. Why: partial writes and aborted transaction state break the operation's contract. [PG-TRANSACTIONS]
- MUST identify database failures by SQLSTATE and structured constraint fields instead of message text. Why: error wording can change with PostgreSQL versions and localization. [PG-TRANSACTIONS]
- MUST retry the complete transaction and its decision logic after a retryable serialization failure, with a bounded retry policy. Why: retrying only the final statement reuses decisions from an invalid snapshot. [PG-TRANSACTIONS]
- MUST set a trusted search_path with pg_temp last for SECURITY DEFINER functions and restrict their EXECUTE grants in the creation transaction. Why: object shadowing or default PUBLIC access can expose elevated privileges. [PG-FUNCTIONS]
- MUST test SQL behavior against PostgreSQL with NULLs, duplicate join keys, empty results, and relevant time boundaries. Why: parser success cannot establish relational or temporal correctness. [PG-PITFALLS] [PG-CONSTRAINTS] [SQLFLUFF]

## When to read more

- Before a change bigger than one function, read [references/guide.md](references/guide.md), the section for what you're doing.
- For naming basics, errors, tests, commits, secrets, and agent workflow, read [references/shared.md](references/shared.md).
- To set up tooling, copy or merge the files in [references/config/](references/config/) into your repository, then read the guide's Tooling section. Use the project's own source files and test fixtures.
- For worked controls, read [transactional schema](references/examples/001_create_artifacts.sql), [concurrent index migration](references/examples/002_index_artifacts.sql), [CTEs and explicit joins](references/examples/collection_totals.sql), [correlated exclusion](references/examples/empty_collections.sql).

## Sources

See [references/sources.md](references/sources.md) for sources, licenses, source tags, and changes. Unofficial: not affiliated with or endorsed by any source's owner.
