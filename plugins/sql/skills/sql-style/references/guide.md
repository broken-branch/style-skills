# SQL style guide

Scope: PostgreSQL 18 application queries, schema definitions, and migrations; SQLFluff 4.5.0 with the PostgreSQL dialect. Plain SQL is the baseline; dbt/Jinja and procedural function bodies need separate integration. The reference client is PostgreSQL 18.6; a consuming repository pins its server patch release.
Baseline: [shared rules](shared.md), including dependencies, commits, versioning, review, and AI agent workflow.
MUST means required; PREFER means the default, with a reason recorded for departures.
Source tags resolve in [source credits](sources.md#source-tags).

Rules tagged [HOLYWELL-SQL] draw on Simon Holywell's SQL Style Guide (CC BY-SA 4.0) in our own words; none of its text is reproduced. The original wording in this house guide is licensed CC BY 4.0.

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

## Tooling

| Purpose | Tool and version | Config file | Repository command |
| --- | --- | --- | --- |
| Formatter | SQLFluff 4.5.0; lint is the nonmutating check, fix applies available corrections | [.sqlfluff](config/.sqlfluff) | `sqlfluff lint --ignore-local-config --config .sqlfluff <sql-files>` |
| Linter | SQLFluff 4.5.0, explicit 65-rule profile | [.sqlfluff](config/.sqlfluff) | `sqlfluff lint --ignore-local-config --config .sqlfluff <sql-files>` |
| Build / type checks | PostgreSQL 18 and psql 18.6 | Project schema and queries in an explicitly selected disposable test database | Project's database verification command; use `psql -X -v ON_ERROR_STOP=1` for scripts |
| Tests | Project's PostgreSQL integration runner | Data fixtures, result assertions, and migration tests | Project's declared SQL integration test command |

Mechanical formatting: the formatter handles this.

Not yet run against SQLFluff 4.5.0 or PostgreSQL 18. Validate the profile with the pinned tool and run schema, query-result, and migration tests against an explicitly selected disposable database before adoption.

- MUST use the PostgreSQL dialect and raw templater for plain SQL files; give dbt/Jinja projects a separately configured compatible templater. Why: parsing the wrong dialect or unrendered template can miss errors or change valid SQL. [SQLFLUFF-CONFIG]
- MUST treat SQLFluff parse/templating errors and skipped large files as failed checks. Why: a skipped statement has no demonstrated lint coverage. [SQLFLUFF-CONFIG]
- MUST run psql scripts with -X and ON_ERROR_STOP=1. Why: personal startup files and psql's default continuation after SQL errors make script results unreliable. [PG-PSQL]
- MUST inspect semantic effects of SQLFluff fixes to joins, aliases, casts, and CASE expressions, then lint again. Why: automated rewriting cannot establish application contracts or schema-dependent behavior. [SQLFLUFF] [GITLAB-SQL]

### Configured rule coverage

These are diagnostic descriptions, not additional prose formatting rules. The IDs exactly match the explicit `rules` setting. The profile inherits other options from the pinned 4.5.0 defaults. [SQLFLUFF] [SQLFLUFF-CONFIG]

| Rule ID | What the selected configuration catches |
| --- | --- |
| `AL01` | Implicit table aliases; explicit AS selected. |
| `AL02` | Implicit column aliases; explicit AS selected. |
| `AL03` | Unnamed computed SELECT outputs, including single targets; named CTE column lists and certain simple casts are exempt. |
| `AL04` | Duplicate relation aliases in a query scope. |
| `AL05` | Unreferenced relation aliases. |
| `AL06` | Relation aliases shorter than four characters; meaning still needs review. |
| `AL08` | Duplicate output aliases. |
| `AL09` | Exact column self-aliases. |
| `AL10` | Derived FROM relations without aliases. |
| `AM01` | SELECT DISTINCT combined with GROUP BY. |
| `AM02` | UNION without explicit ALL or DISTINCT. |
| `AM03` | Mixed explicit and implicit ORDER BY directions. |
| `AM04` | Wildcards whose output width cannot be resolved from the SQL. |
| `AM05` | Bare JOIN without INNER; OUTER remains optional for outer joins. |
| `AM06` | Positional GROUP BY/ORDER BY references; window ORDER BY is outside this check. |
| `AM07` | Set-operation branches with different known column counts. |
| `AM08` | Implicit cross joins lacking a join condition. |
| `AM09` | LIMIT/OFFSET without ORDER BY; unique tie-breakers still need review. |
| `CP01` | Keywords outside the configured uppercase policy. |
| `CP02` | Unquoted identifiers outside the lowercase policy; word separation and quoted names remain manual. |
| `CP03` | Function names outside the uppercase policy. |
| `CP04` | Boolean/NULL literals outside the uppercase policy. |
| `CP05` | Type names outside the uppercase policy. |
| `CV01` | Inequality spelling other than the selected ANSI <>. |
| `CV02` | IFNULL/NVL where COALESCE expresses the fallback. |
| `CV03` | A final SELECT-list comma forbidden by PostgreSQL. |
| `CV04` | COUNT(0)/COUNT(1) instead of the selected row-count form COUNT(*). |
| `CV05` | Equality/inequality comparisons to NULL instead of IS [NOT] NULL. |
| `CV06` | Missing final statement terminators. |
| `CV07` | Redundant parentheses enclosing a whole statement. |
| `CV08` | RIGHT JOIN instead of the selected LEFT JOIN orientation. |
| `CV11` | Cast notation inconsistent with selected CAST(expression AS type). |
| `CV12` | Join predicates placed in WHERE instead of JOIN ... ON. |
| `LT01` | Spacing differences under the formatter policy. |
| `LT02` | Indentation differences under the formatter policy. |
| `LT03` | Operator placement differences under the formatter policy. |
| `LT04` | Comma placement differences under the formatter policy. |
| `LT05` | Lines exceeding the configured formatter width. |
| `LT06` | Function-call spacing differences. |
| `LT07` | CTE closing-bracket layout differences. |
| `LT08` | CTE separation differences. |
| `LT09` | SELECT-target layout differences. |
| `LT10` | SELECT-modifier placement differences. |
| `LT11` | Set-operator layout differences. |
| `LT12` | End-of-file newline differences. |
| `LT13` | Leading file whitespace. |
| `LT14` | Clause-keyword layout differences. |
| `LT15` | Excess consecutive blank lines. |
| `RF01` | References to relations or aliases absent from visible FROM scope; no database catalog lookup. |
| `RF02` | Unqualified column references with multiple visible relations, including outer references. |
| `RF03` | Inconsistent qualification in single-relation queries. |
| `RF04` | Keywords used as unquoted identifiers; necessary existing quoted names are exempt. |
| `RF05` | Special characters in unquoted identifiers; existing quoted names are exempt. |
| `RF06` | Unnecessary identifier quotes, preserving quotes whose removal would change case-sensitive meaning. |
| `ST01` | Redundant ELSE NULL. |
| `ST02` | Simplifiable CASE expressions. |
| `ST03` | Unused CTEs; 4.5.0 explicitly exempts data-modifying CTEs. |
| `ST04` | CASE nested solely in another CASE's ELSE. |
| `ST05` | Relation subqueries in JOIN; FROM subqueries are allowed. |
| `ST07` | JOIN USING; the house default exposes both operands through ON. |
| `ST08` | DISTINCT written as a function-like expression. |
| `ST09` | Simple qualified join comparisons with the later relation first. |
| `ST10` | Constant predicates that need inspection for mistakes or deliberate intent. |
| `ST11` | Unreferenced outer-joined relations; cardinality effects need manual review. |
| `ST12` | Consecutive statement terminators. |

Omitted IDs: `AL07` would forbid useful aliases; `CV09` has no blanket blocked-word policy; `CV10` targets dialects with two interchangeable string quote forms; `CV13` imposes a dbt final-star model; `JJ01` needs a Jinja-derived templater; `ST06` can reorder positional result contracts. Optional `RF07` remains off, with window-name resolution checked by PostgreSQL. `PG01`/`PG02` are enabled in the separate migration pass below, not in the general query/schema profile. `OR01` and `TQ01`–`TQ04` concern other dialects. [SQLFLUFF]

AL06 turns the alias-length preference into a diagnostic; a justified shorter domain alias needs an explained, scoped `-- noqa: AL06`. [SQLFLUFF]

Manual review covers identifier word boundaries and suffixes, type choices, timestamp ranges, NULL and NOT EXISTS semantics, key/constraint design, join cardinality, output contracts, unique pagination ordering, transaction retries, privileges, and execution plans. AM04 can accept a statically known CTE wildcard even where a public output contract requires an explicit list. AL03 has documented exemptions; it does not establish the quality or completeness of output names. [SQLFLUFF] [PG-PITFALLS] [PG-CONSTRAINTS] [PG-TRANSACTIONS] [PG-FUNCTIONS]

## Naming

- MUST use unquoted lowercase snake_case for new schema identifiers and avoid keyword names. Why: PostgreSQL folds unquoted names to lowercase and quoted mixed case creates fragile references. [PG-PITFALLS] [GITLAB-SQL]
- MUST preserve exact required quotation and spelling when referencing existing quoted identifiers. Why: removing semantic quotes can select a different object or make a valid query fail. [PG-PITFALLS] [SQLFLUFF]
- PREFER collective or plural relation names, singular column names, and entity-qualified keys such as customer_id. Why: identifiers distinguish relations from individual attributes and remain clear after joins. [HOLYWELL-SQL] [GITLAB-SQL]
- PREFER _at for instant timestamps, _date for dates, _id for identifiers, and is_/has_/does_ for Boolean columns. Why: names reveal SQL value semantics without opening the schema. [GITLAB-SQL] [HOLYWELL-SQL]
- PREFER full relation names or descriptive aliases of at least four characters. Why: readable references preserve the query's domain meaning. [GITLAB-SQL] [SQLFLUFF]
- MUST use explicit AS for every table or column alias. Why: alias declarations remain distinct from expressions and relation names. [HOLYWELL-SQL] [GITLAB-SQL] [SQLFLUFF]
- MUST name computed result columns and enumerate columns at application, view, and export boundaries. Why: consumers need a stable output shape and meaningful field names. [HOLYWELL-SQL] [SQLFLUFF]

## Files and layout

- PREFER named CTEs for independent query stages while retaining subqueries needed for correlation or LATERAL semantics. Why: logical stages should be readable without changing their dependencies. [GITLAB-SQL] [PG-WITH]
- MUST qualify column references when a query uses multiple relations, including correlated outer references. Why: schema additions must not make a reference ambiguous. [GITLAB-SQL] [SQLFLUFF]
- MUST use explicit JOIN syntax and join types; use CROSS JOIN only for an intentional Cartesian product. Why: the relationship and row multiplication remain visible. [GITLAB-SQL] [SQLFLUFF]
- PREFER LEFT JOIN orientation and explicit ON keys over RIGHT JOIN or USING, preserving merged-key semantics when changing existing queries. Why: a consistent preserved side and visible operands simplify review. [GITLAB-SQL] [SQLFLUFF]
- MUST use named references or expressions instead of numeric positions in GROUP BY and ORDER BY. Why: editing the SELECT list must not silently change grouping or sorting. [SQLFLUFF]
- PREFER non-aggregate outputs before aggregates in new result shapes, preserving established output positions. Why: grouping dimensions remain easy to scan without breaking positional consumers. [GITLAB-SQL] [SQLFLUFF]

### Migrations

- MUST use `CREATE INDEX CONCURRENTLY` and `DROP INDEX CONCURRENTLY` outside transaction blocks on existing populated tables; document an alternative lock plan for operations or table kinds that cannot use them. Why: ordinary index DDL can block live traffic. [SQLFLUFF] [PG-CREATEINDEX] [PG-DROPINDEX]
- MUST stage new foreign keys and CHECK constraints on existing populated tables with `NOT VALID`, commit that change, then run `VALIDATE CONSTRAINT` separately after correcting invalid rows. Why: validation scans should not extend the initial schema-change lock. [PG-ALTERTABLE] [SQLFLUFF]
- MUST set a bounded migration `lock_timeout`, using `SET LOCAL` inside transactions and session `SET`/`RESET` around concurrent DDL; choose the timeout for the deployment. Why: a waiting schema lock can queue ordinary requests behind it. [PG-LOCK-TIMEOUT] [PG-LOCKING]
- MUST keep data backfills outside schema-change transactions, using bounded resumable batches and a checked completion condition before validation. Why: long writes prolong lock lifetimes and make rollback and recovery expensive. [PG-ALTERTABLE] [PG-LOCKING]
- MUST review migration transaction boundaries, lock levels, failure recovery, and live-table tests; use concurrent REINDEX or materialized-view refresh when supported and appropriate. Why: `CONCURRENTLY` has prerequisites and failed index builds can leave invalid indexes. [SQLFLUFF] [PG-CREATEINDEX] [PG-ALTERTABLE] [PG-MAINTENANCE]

PostgreSQL documents [concurrent index restrictions and invalid-index recovery](https://www.postgresql.org/docs/18/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY), [staged constraint validation](https://www.postgresql.org/docs/18/sql-altertable.html), and [lock_timeout](https://www.postgresql.org/docs/18/runtime-config-client.html#GUC-LOCK-TIMEOUT). Bounded resumable backfills are house policy derived from these validation and lock-lifetime constraints. Partitioned tables and constraint-owned indexes need a specific plan; these defaults do not make unsupported concurrent operations valid.

Run the general profile on all SQL, then run the separate [migration profile](config/migrations.sqlfluff) on migration files: `sqlfluff lint --ignore-local-config --config migrations.sqlfluff <migration-files>`. Both passes must succeed. The separate profile explicitly selects `PG01`/`PG02` and sets each `force_enable = True`; it does not replace the general 65-rule gate. Migration transaction guidance (upstream-only; not bundled) illustrates distinct transactions. [SQLFLUFF-CONFIG]

| Migration rule | Coverage and limits |
| --- | --- |
| `PG01` (`postgres.excessive_locks`) | Missing concurrent index/reindex/refresh forms; the pinned check excludes `CREATE UNIQUE INDEX`, which still needs review. |
| `PG02` (`postgres.not_valid_foreign_key`) | Foreign keys added without `NOT VALID`; CHECK staging, later validation, timeouts, and transaction boundaries remain review duties. |

## Types and data

- MUST store instants as TIMESTAMPTZ; reserve TIMESTAMP WITHOUT TIME ZONE for deliberate wall-clock values. Why: an unzoned timestamp cannot identify a moment across time zones. [PG-PITFALLS]
- MUST supply an explicit zone or offset when converting external local timestamps into instants, and store any required original zone separately. Why: TIMESTAMPTZ represents an instant rather than retaining the original zone label. [PG-PITFALLS]
- PREFER TEXT for PostgreSQL strings, using length or format constraints only for actual domain limits. Why: CHAR padding and arbitrary VARCHAR limits add unwanted behavior. [PG-PITFALLS]
- MUST represent exact monetary amounts with NUMERIC and an explicit currency contract, using a currency column when currencies vary. Why: floating-point approximation and MONEY's locale assumptions lose required meaning. [PG-PITFALLS] [HOLYWELL-SQL]
- MUST group and sum monetary amounts by currency unless an explicit conversion has produced a common currency. Why: adding unlike currencies does not produce a meaningful total. [PG-PITFALLS]
- PREFER PostgreSQL INTEGER/BIGINT, NUMERIC, BOOLEAN, TEXT, and the appropriate temporal type over copying Snowflake aliases. Why: type names and semantics must match the execution engine. [HOLYWELL-SQL] [GITLAB-SQL] [PG-PITFALLS]
- PREFER GENERATED ALWAYS AS IDENTITY for new generated integer keys, with PRIMARY KEY or UNIQUE as appropriate. Why: identity manages generation but uniqueness still needs a constraint. [PG-PITFALLS] [PG-CONSTRAINTS]
- MUST enforce relational invariants with primary/unique keys, foreign keys, NOT NULL, and CHECK as appropriate; CHECK alone does not reject NULL. Why: every writer must preserve the same valid database states. [PG-CONSTRAINTS]
- MUST express cross-row and cross-table invariants through UNIQUE, EXCLUDE, or FOREIGN KEY constraints where possible, keeping CHECK conditions row-local. Why: PostgreSQL does not continuously recheck other rows when a CHECK expression depends on them. [PG-CONSTRAINTS]

## Errors

- MUST wrap related writes that must succeed together in one transaction and roll back a failed transaction before reuse. Why: partial writes and aborted transaction state break the operation's contract. [PG-TRANSACTIONS]
- PREFER a savepoint when a known statement failure must be recoverable within a larger transaction. Why: ROLLBACK TO SAVEPOINT restores a usable transaction without committing partial recovery. [PG-TRANSACTIONS]
- MUST identify database failures by SQLSTATE and structured constraint fields instead of message text. Why: error wording can change with PostgreSQL versions and localization. [PG-TRANSACTIONS]
- MUST retry the complete transaction and its decision logic after a retryable serialization failure, with a bounded retry policy. Why: retrying only the final statement reuses decisions from an invalid snapshot. [PG-TRANSACTIONS]
- MUST distinguish serialization_failure (40001), deadlock_detected (40P01), and domain constraint failures before choosing recovery. Why: a uniqueness failure can be persistent invalid input rather than a transient concurrency conflict. [PG-TRANSACTIONS]

## Comments and docs

- PREFER documenting a reporting query's row grain, join cardinalities, currency, and time-window interpretation beside its definition. Why: an apparently valid aggregate can count a different business population than intended. [GITLAB-SQL] [PG-PITFALLS]
- PREFER explicit names for domain CHECK constraints and other constraints whose generated names would be unclear. Why: PostgreSQL error fields and migrations can identify the exact invariant. [HOLYWELL-SQL] [PG-CONSTRAINTS] [PG-TRANSACTIONS]

## Testing

- MUST test SQL behavior against PostgreSQL with NULLs, duplicate join keys, empty results, and relevant time boundaries. Why: parser success cannot establish relational or temporal correctness. [PG-PITFALLS] [PG-CONSTRAINTS] [SQLFLUFF]
- MUST include exactly-on-boundary timestamps and multiple time zones in tests for instant-based periods. Why: inclusive endpoints, session-zone assumptions, and daylight-saving transitions expose temporal mistakes. [PG-PITFALLS]
- MUST exercise constraint rejection and rollback paths when adding write invariants. Why: happy-path inserts cannot establish database-enforced validity or atomicity. [PG-CONSTRAINTS] [PG-TRANSACTIONS]
- MUST test intended duplicate preservation, unmatched outer-join rows, and output column order when changing joins or set operations. Why: equal-looking queries can have different cardinalities and positional contracts. [SQLFLUFF] [GITLAB-SQL]

## Performance

- PREFER an index on foreign-key referencing columns unless measured access patterns show it is unnecessary. Why: PostgreSQL does not create this index automatically, and referenced-row updates/deletes otherwise scan the referencing table. [PG-CONSTRAINTS]

- PREFER PostgreSQL EXPLAIN (ANALYZE, BUFFERS) on representative disposable data when diagnosing a query plan. Why: actual row counts, loops, and buffer use reveal estimation and access-path costs. [PG-EXPLAIN]
- MUST account for actual execution and side effects before running EXPLAIN ANALYZE on a statement. Why: ANALYZE executes writes and invoked functions as well as reporting their plan. [PG-EXPLAIN]
- PREFER the planner's default CTE folding/materialization until a measured plan justifies MATERIALIZED or NOT MATERIALIZED. Why: forcing reuse can prevent predicate pushdown, while forced inlining can repeat expensive work. [PG-WITH]
- PREFER WHERE for row predicates and HAVING for aggregate predicates, preserving outer-join semantics when moving conditions. Why: each clause filters a different stage of relational evaluation. [GITLAB-SQL] [SQLFLUFF]

## Security

- PREFER SECURITY INVOKER functions unless the operation needs an explicitly designed privilege boundary. Why: ordinary functions can run with their caller's privileges. [PG-FUNCTIONS]
- MUST set a trusted search_path with pg_temp last for SECURITY DEFINER functions and restrict their EXECUTE grants in the creation transaction. Why: object shadowing or default PUBLIC access can expose elevated privileges. [PG-FUNCTIONS]

For example, a definer function can set `search_path = pg_catalog, trusted_app, pg_temp`; `trusted_app` is appropriate only when callers cannot create objects there. Creation, revocation of default PUBLIC execution, and explicit grants belong in one transaction. [PG-FUNCTIONS]

## Language-specific pitfalls

- MUST test nullness with IS NULL or IS NOT NULL and choose COALESCE only when the fallback has domain meaning. Why: NULL comparisons and indiscriminate defaults can hide unknown data. [SQLFLUFF] [PG-CONSTRAINTS]
- PREFER correlated NOT EXISTS for subquery exclusions, explicitly deciding how nullable outer keys behave. Why: a NULL in a NOT IN result can suppress every candidate row. [PG-PITFALLS]
- MUST use half-open timestamp windows, value >= start AND value < end, for adjacent periods. Why: inclusive upper bounds double-count boundary events. [PG-PITFALLS]
- PREFER BETWEEN only for deliberately inclusive discrete ranges. Why: the inclusive endpoints can be appropriate for integers or dates but need to be intentional. [PG-PITFALLS]
- MUST choose UNION ALL or UNION DISTINCT explicitly and preserve positional output contracts. Why: duplicate elimination and column position affect the result's meaning. [GITLAB-SQL] [SQLFLUFF]
- MUST give paginated or limited application results a deterministic ORDER BY with a unique tie-breaker. Why: tied or unordered rows do not define a repeatable subset. [SQLFLUFF]
- PREFER CASE, COALESCE, EXTRACT, and CAST for their standard operations rather than Snowflake IFF/IFNULL/date helpers. Why: the selected PostgreSQL engine supports these forms with clear semantics. [HOLYWELL-SQL] [GITLAB-SQL] [SQLFLUFF]
- MUST distinguish COUNT(*) for rows from COUNT(column) for non-null values. Why: a nullable column changes the population being counted. [SQLFLUFF]
- MUST use DATE_TRUNC when truncation is intended rather than timestamp precision declarations, and avoid TIMETZ/CURRENT_TIME for instants. Why: precision declarations round and a time with no date cannot identify an instant. [PG-PITFALLS]
- MUST use a named time zone or an INTERVAL-typed fixed offset with AT TIME ZONE rather than assuming a signed text offset has ISO direction. Why: text zone specifications can use PostgreSQL's POSIX sign convention. [PG-PITFALLS]
- PREFER foreign-key relationships and native partitioning over table inheritance, and triggers over handwritten rewrite rules. Why: PostgreSQL already provides clearer mechanisms for those relationships and effects. [PG-PITFALLS]
- MUST preserve intentional data-modifying CTEs even when their returned rows are unused. Why: PostgreSQL executes those writes independently of whether the primary query consumes their output. [PG-WITH] [SQLFLUFF]

A NOT EXISTS exclusion can include an outer row whose key is NULL; add an outer IS NOT NULL condition if the business rule excludes it. A fixed non-null NOT IN list remains valid for deliberate exclusion. These are semantic choices, not interchangeable text rewrites. [PG-PITFALLS]

## Where the sources disagree

Where the sources disagree, the following house choices apply. Each choice states the adopted behavior and its reason.

- MUST use half-open timestamp windows for adjacent periods (1), choosing PostgreSQL's range warning over Holywell's general BETWEEN preference. Why: a shared endpoint must not belong to both periods. [PG-PITFALLS] [HOLYWELL-SQL]
- MUST use a currency column when monetary values vary by currency (2), following PostgreSQL's numeric-plus-currency model over Holywell's blanket rejection of companion unit fields. Why: the amount alone cannot identify its currency. [PG-PITFALLS] [HOLYWELL-SQL]
- MUST store instants as TIMESTAMPTZ (3), following PostgreSQL instead of copying GitLab's Snowflake TIMESTAMP/UTC convention. Why: Snowflake's timezone-free default does not provide PostgreSQL instant semantics. [PG-PITFALLS] [GITLAB-SQL]
- PREFER PostgreSQL types appropriate to the domain (4), retaining Holywell's standard exact numeric types instead of GitLab's Snowflake NUMBER/FLOAT/VARCHAR aliases. Why: portability yields to the selected backend's actual semantics. [HOLYWELL-SQL] [GITLAB-SQL] [PG-PITFALLS]
- PREFER TEXT and explicit domain constraints (5), choosing PostgreSQL's guidance over CHAR/VARCHAR as generic options in Holywell's portable appendix. Why: padding and arbitrary maximum lengths are not useful defaults. [PG-PITFALLS] [HOLYWELL-SQL]
- PREFER CASE and EXTRACT for standard conditionals and date-part extraction (6), following Holywell over GitLab's Snowflake IFF/native-helper preference. Why: the chosen expressions have direct PostgreSQL meanings. [HOLYWELL-SQL] [GITLAB-SQL]
- MUST choose COALESCE when a null fallback is needed (7), following SQLFluff CV02 over GitLab's IFNULL-over-NVL policy. Why: PostgreSQL supplies COALESCE without vendor-specific compatibility functions. [SQLFLUFF] [GITLAB-SQL]
- PREFER descriptive aliases with at least four characters (8), following GitLab over Holywell's initials and numeric collision suffixes. Why: the lintable minimum discourages opaque shorthand. [GITLAB-SQL] [HOLYWELL-SQL] [SQLFLUFF]
- PREFER useful relation aliases (9), retaining both prose guides' permission and leaving SQLFluff's optional AL07 ban disabled. Why: self-joins and role-specific names benefit from aliases. [HOLYWELL-SQL] [GITLAB-SQL] [SQLFLUFF]
- MUST use explicit AS for aliases (10), adopting both prose guides and the explicit AL01/AL02 setting instead of SQLFluff's optional implicit policy. Why: alias declarations remain easy to identify. [HOLYWELL-SQL] [GITLAB-SQL] [SQLFLUFF]
- PREFER the checked-in SQLFluff layout policy (11) over Holywell's manual keyword river and GitLab's selective alias alignment. Why: one formatter owns layout and prevents alignment churn; the formatter handles this. [HOLYWELL-SQL] [GITLAB-SQL] [SQLFLUFF-CONFIG]
- PREFER _at for timestamps and _date for dates (12), following GitLab's explicit distinction rather than extending Holywell's _date examples to timestamps. Why: the suffix exposes temporal granularity; Holywell does not forbid _at. [GITLAB-SQL] [HOLYWELL-SQL]
- PREFER CTEs for independent stages (13), taking GitLab's organization over Holywell's accepted nested layout and enabling ST05 only for JOIN subqueries. Why: FROM, correlated, and LATERAL cases still need their semantics preserved. [GITLAB-SQL] [HOLYWELL-SQL] [SQLFLUFF] [PG-WITH]
- MUST use the configured ANSI <> inequality spelling (14), selecting SQLFluff CV01's ANSI option over GitLab's != preference. Why: one supported spelling is enforceable across PostgreSQL queries. [GITLAB-SQL] [SQLFLUFF]
- PREFER explicit ON keys (15), adopting GitLab's visible-key intent and SQLFluff ST07 for PostgreSQL without importing Snowflake's failure claim or ClickHouse's exemption. Why: both relation operands stay explicit; existing USING semantics require care. [GITLAB-SQL] [SQLFLUFF]
- PREFER non-aggregate outputs before aggregates for new result shapes (16), keeping GitLab's prose preference and leaving SQLFluff ST06's broader reorder policy disabled. Why: established output positions can be part of an application or set-operation contract. [GITLAB-SQL] [SQLFLUFF]
- MUST avoid unnecessary identifier quotes while preserving semantic quotes (17), following both prose guides and RF06's case-sensitive removal setting over optional quote-everything policy. Why: new names stay simple without changing existing object identity. [HOLYWELL-SQL] [GITLAB-SQL] [SQLFLUFF]
- MUST use the configured uppercase keyword policy (18), adopting both prose guides rather than SQLFluff's optional lowercase policy. Why: a fixed CP01 choice produces consistent automated output. [HOLYWELL-SQL] [GITLAB-SQL] [SQLFLUFF]

- MUST use named GROUP BY/ORDER BY references (conflict 19), choosing SQLFluff AM06 `explicit` over GitLab's permission for positions. Why: editing the SELECT list must not silently regroup or reorder results. [GITLAB-SQL] [SQLFLUFF]
