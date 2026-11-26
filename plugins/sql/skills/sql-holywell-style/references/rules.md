# Simon Holywell SQL rules (condensed)

Every rule in Simon Holywell’s SQL Style Guide. Examples and the dated keyword glossary are omitted.

Each rule cites its original section, with parent headings where needed to distinguish repeated names. Recommendations and optional choices retain their original strength. Apply syntax and type choices only where the target database supports them.

## Quick rules

- Prefer SQL-standard functions when an engine-specific alternative is unnecessary. — [General](https://www.sqlstyle.guide/#general).
- Omit SQL that adds no meaning, including needless quoting, parentheses, and derivable conditions. — [General](https://www.sqlstyle.guide/#general).

## Naming

- Give identifiers clear meanings and follow a consistent naming scheme. — [General](https://www.sqlstyle.guide/#general).
- Do not capitalize word boundaries in the camelCase style. — [General](https://www.sqlstyle.guide/#general).
- Leave object-kind prefixes and Hungarian type encodings out of names. — [General](https://www.sqlstyle.guide/#general).
- Favor a natural collective term when a plural label would be less suitable. — [General](https://www.sqlstyle.guide/#general).
- Prefer identifiers that need no quoting; otherwise use SQL-92 double quotes, enabling the engine's support if necessary. — [General](https://www.sqlstyle.guide/#general).
- Select distinct identifiers and exclude the target dialect's reserved words. — [Naming conventions: General](https://www.sqlstyle.guide/#general-1).
- Keep each identifier within 30 bytes, accounting for multibyte characters. — [Naming conventions: General](https://www.sqlstyle.guide/#general-1).
- Begin identifiers with an alphabetic character. — [Naming conventions: General](https://www.sqlstyle.guide/#general-1).
- Leave no trailing underscore on an identifier. — [Naming conventions: General](https://www.sqlstyle.guide/#general-1).
- Restrict identifier characters to letters, digits, and `_`. — [Naming conventions: General](https://www.sqlstyle.guide/#general-1).
- Avoid adjacent underscores within identifiers. — [Naming conventions: General](https://www.sqlstyle.guide/#general-1).
- Put an underscore wherever the identifier's words would normally have a space. — [Naming conventions: General](https://www.sqlstyle.guide/#general-1).
- Spell names out unless a necessary abbreviation is familiar to readers. — [Naming conventions: General](https://www.sqlstyle.guide/#general-1).
- Name tables with collective nouns when possible, falling back to plurals. — [Tables](https://www.sqlstyle.guide/#tables).
- Omit table-kind prefixes, including `tbl`, from table identifiers. — [Tables](https://www.sqlstyle.guide/#tables).
- Ensure a table's name differs from every column name within it. — [Tables](https://www.sqlstyle.guide/#tables).
- Prefer a relationship table's purpose as its name over joining its endpoint names. — [Tables](https://www.sqlstyle.guide/#tables).
- Give columns singular rather than plural names. — [Columns](https://www.sqlstyle.guide/#columns).
- Prefer a descriptive primary identifier over the unqualified name `id`. — [Columns](https://www.sqlstyle.guide/#columns).
- Default column identifiers to lowercase, allowing meaningful exceptions such as proper nouns. — [Columns](https://www.sqlstyle.guide/#columns).
- Choose aliases with a recognizable connection to the underlying object or expression. — [Aliasing or correlations](https://www.sqlstyle.guide/#aliasing-or-correlations).
- Usually derive correlation names from the initials of the original name's words. — [Aliasing or correlations](https://www.sqlstyle.guide/#aliasing-or-correlations).
- Resolve an alias collision by adding a numeric suffix. — [Aliasing or correlations](https://www.sqlstyle.guide/#aliasing-or-correlations).
- Introduce each alias with an explicit `AS`. — [Aliasing or correlations](https://www.sqlstyle.guide/#aliasing-or-correlations).
- Give a derived result the same kind of name you would assign a schema column. — [Aliasing or correlations](https://www.sqlstyle.guide/#aliasing-or-correlations).
- Make the operation visible through a verb in each procedure's name. — [Stored procedures](https://www.sqlstyle.guide/#stored-procedures).
- Exclude `sp_` and other object-kind prefixes from procedure names. — [Stored procedures](https://www.sqlstyle.guide/#stored-procedures).
- Mark unique-identifier columns with the suffix `_id`. — [Uniform suffixes](https://www.sqlstyle.guide/#uniform-suffixes).
- Mark flags and other state values with `_status`. — [Uniform suffixes](https://www.sqlstyle.guide/#uniform-suffixes).
- Mark values summed across a collection with `_total`. — [Uniform suffixes](https://www.sqlstyle.guide/#uniform-suffixes).
- Mark a field holding any kind of number with `_num`. — [Uniform suffixes](https://www.sqlstyle.guide/#uniform-suffixes).
- Identify a field that holds a name with `_name`. — [Uniform suffixes](https://www.sqlstyle.guide/#uniform-suffixes).
- Identify contiguous sequence values with `_seq`. — [Uniform suffixes](https://www.sqlstyle.guide/#uniform-suffixes).
- Identify a field recording a date with `_date`. — [Uniform suffixes](https://www.sqlstyle.guide/#uniform-suffixes).
- Distinguish a count by the ending `_tally`. — [Uniform suffixes](https://www.sqlstyle.guide/#uniform-suffixes).
- Distinguish a size measurement by the ending `_size`. — [Uniform suffixes](https://www.sqlstyle.guide/#uniform-suffixes).
- Identify addresses, whether physical or logical, with `_addr`. — [Uniform suffixes](https://www.sqlstyle.guide/#uniform-suffixes).
- Supply readable constraint names, allowing clear engine-generated names for primary, foreign, and unique keys. — [Defining constraints: General](https://www.sqlstyle.guide/#general-2).

## Files and layout

- Use indentation and spacing to make SQL structure easy to read. — [General](https://www.sqlstyle.guide/#general).
- Capitalize every reserved SQL keyword in full. — [Reserved words](https://www.sqlstyle.guide/#reserved-words).
- Prefer an unabbreviated keyword when the dialect provides that spelling. — [Reserved words](https://www.sqlstyle.guide/#reserved-words).
- Choose the ANSI keyword when it provides the same operation as an engine-specific one. — [Reserved words](https://www.sqlstyle.guide/#reserved-words).
- Align the ends of root keywords vertically, with their arguments starting to the right of the resulting gap. — [Spaces](https://www.sqlstyle.guide/#spaces).
- Surround `=` with spaces. — [Spaces](https://www.sqlstyle.guide/#spaces).
- Follow each comma with a space. — [Spaces](https://www.sqlstyle.guide/#spaces).
- Put spaces outside single-quoted values, except against enclosing parentheses or a following comma or semicolon. — [Spaces](https://www.sqlstyle.guide/#spaces).
- Break the line before each `AND` and `OR`. — [Line spacing](https://www.sqlstyle.guide/#line-spacing).
- After a query's terminating semicolon, begin the next query on another line. — [Line spacing](https://www.sqlstyle.guide/#line-spacing).
- End each keyword's clause with a line break before the next clause. — [Line spacing](https://www.sqlstyle.guide/#line-spacing).
- Break after a comma when it marks a boundary between meaningful column groups. — [Line spacing](https://www.sqlstyle.guide/#line-spacing).
- Use vertical gaps to distinguish related sections within a larger query. — [Line spacing](https://www.sqlstyle.guide/#line-spacing).
- Place qualified join clauses to the right of the gap separating root keywords from arguments. — [Joins](https://www.sqlstyle.guide/#joins).
- Introduce line breaks where they clarify the grouping of joins. — [Joins](https://www.sqlstyle.guide/#joins).
- Align an unqualified `JOIN` with root keywords on the gap's left side. — [Joins](https://www.sqlstyle.guide/#joins).
- Start subqueries on the argument side of the gap and repeat the normal query layout inside them. — [Subqueries](https://www.sqlstyle.guide/#subqueries).
- When it clarifies nesting, put a closing subquery parenthesis on its own line aligned with the opening parenthesis. — [Subqueries](https://www.sqlstyle.guide/#subqueries).
- Arrange column declarations into a readable order and meaningful groups. — [Create syntax](https://www.sqlstyle.guide/#create-syntax).
- Offset column declarations inside `CREATE` by four spaces. — [Create syntax](https://www.sqlstyle.guide/#create-syntax).
- Position a column's default between its type and any `NOT NULL` declaration. — [Specifying default values](https://www.sqlstyle.guide/#specifying-default-values).
- Lead the table definition with its primary-key declaration immediately after the `CREATE TABLE` header. — [Layout and order](https://www.sqlstyle.guide/#layout-and-order).
- Place a column's constraints directly underneath it, indented to the right of its name. — [Layout and order](https://www.sqlstyle.guide/#layout-and-order).
- Keep a constraint involving multiple columns near those declarations; move it to the definition's end only if needed. — [Layout and order](https://www.sqlstyle.guide/#layout-and-order).
- Finish a table definition with any constraint applying to the table as a whole. — [Layout and order](https://www.sqlstyle.guide/#layout-and-order).
- Order referential actions alphabetically: `ON DELETE` precedes `ON UPDATE`. — [Layout and order](https://www.sqlstyle.guide/#layout-and-order).
- Align corresponding constraint attributes vertically when that makes the definition easier to scan. — [Layout and order](https://www.sqlstyle.guide/#layout-and-order).

## Types and data

- Represent stored dates and times in a form conforming to ISO 8601. — [General](https://www.sqlstyle.guide/#general).
- Prefer `BETWEEN` for a range when it preserves the intended boundary conditions. — [Preferred formalisms](https://www.sqlstyle.guide/#preferred-formalisms).
- Express alternative equality matches with `IN` instead of repeated `OR` comparisons. — [Preferred formalisms](https://www.sqlstyle.guide/#preferred-formalisms).
- Interpret result values with `CASE` before returning them when required, nesting expressions if necessary. — [Preferred formalisms](https://www.sqlstyle.guide/#preferred-formalisms).
- Favor standard data types over engine-specific types when the standard choice suffices. — [Choosing data types](https://www.sqlstyle.guide/#choosing-data-types).
- Default to `NUMERIC` or `DECIMAL`, using `REAL` or `FLOAT` only for necessary floating-point calculations. — [Choosing data types](https://www.sqlstyle.guide/#choosing-data-types).
- Match each default value's type to the column's declared type. — [Specifying default values](https://www.sqlstyle.guide/#specifying-default-values).
- Evaluate how much uniqueness a candidate key provides before selecting it. — [Choosing keys](https://www.sqlstyle.guide/#choosing-keys).
- Choose keys with a consistent type throughout the schema and little need for future type changes. — [Choosing keys](https://www.sqlstyle.guide/#choosing-keys).
- Favor key values whose format can be checked against an established standard. — [Choosing keys](https://www.sqlstyle.guide/#choosing-keys).
- Minimize key complexity while retaining multiple columns when the key needs them. — [Choosing keys](https://www.sqlstyle.guide/#choosing-keys).
- Define at least one key for every table. — [Defining constraints: General](https://www.sqlstyle.guide/#general-2).
- Enforce a known string pattern with constraints using `LIKE` or `SIMILAR TO`. — [Validation](https://www.sqlstyle.guide/#validation).
- Encode known numeric bounds in a `CHECK` constraint. — [Validation](https://www.sqlstyle.guide/#validation).
- For domains requiring positive values, at least check that the number exceeds zero. — [Validation](https://www.sqlstyle.guide/#validation).
- Give distinct checks separate `CHECK` clauses so failures are easier to diagnose. — [Validation](https://www.sqlstyle.guide/#validation).
- Make a value column's units apparent without requiring a separate units column. — [Designs to avoid](https://www.sqlstyle.guide/#designs-to-avoid).
- Apply `CHECK` constraints to exclude values outside the column's intended domain. — [Designs to avoid](https://www.sqlstyle.guide/#designs-to-avoid).
- For character data, consider the appendix's portable choices `CHAR`, `CLOB`, and `VARCHAR`. — [Appendix: Column data types](https://www.sqlstyle.guide/#column-data-types).
- Consider `BIGINT`, `DECIMAL`, `DECFLOAT`, `INTEGER`, `NUMERIC`, and `SMALLINT` from the appendix's exact-number list, verifying the target type's semantics. — [Appendix: Column data types](https://www.sqlstyle.guide/#column-data-types).
- For approximate numeric calculations, consider `DOUBLE PRECISION`, `FLOAT`, or `REAL`. — [Appendix: Column data types](https://www.sqlstyle.guide/#column-data-types).
- Consider `DATE`, `TIME`, and `TIMESTAMP` for temporal columns. — [Appendix: Column data types](https://www.sqlstyle.guide/#column-data-types).
- Consider `BINARY`, `BLOB`, and `VARBINARY` for binary columns where the engine supports them. — [Appendix: Column data types](https://www.sqlstyle.guide/#column-data-types).
- Consider the appendix's further choices `BOOLEAN`, `INTERVAL`, and `XML` when suitable for the data and engine. — [Appendix: Column data types](https://www.sqlstyle.guide/#column-data-types).

## Comments and docs

- Explain SQL where useful with `/* ... */` comments when practical, otherwise using `--` through the end of the line. — [General](https://www.sqlstyle.guide/#general).

## Performance

- Prefer a schema that avoids dependence on `UNION` or temporary tables where a better design can remove that need. — [Preferred formalisms](https://www.sqlstyle.guide/#preferred-formalisms).

## Language-specific pitfalls

- Design relational structures on their own terms instead of directly importing object-oriented principles. — [General](https://www.sqlstyle.guide/#general).
- Avoid modeling relational tables as an object-oriented inheritance hierarchy. — [Designs to avoid](https://www.sqlstyle.guide/#designs-to-avoid).
- Choose a product designed for schemaless data rather than recreating one through entity–attribute–value tables. — [Designs to avoid](https://www.sqlstyle.guide/#designs-to-avoid).
- Keep one logical dataset together instead of arbitrarily dividing tables by date or region and needing `UNION` to reunite them. — [Designs to avoid](https://www.sqlstyle.guide/#designs-to-avoid).

The source's [Reserved keyword reference](https://www.sqlstyle.guide/#reserved-keyword-reference) names older database releases, including PostgreSQL 8.1, SQL Server 2000, and Oracle 10.2. Its list is not a current dialect reference. The type appendix is a set of source recommendations, not a guarantee of support or identical behavior across engines.

## Where the sources disagree

This package follows one guide; it does not blend in the house guide's different choices. No unresolved source conflicts in this guide's scope. Existing project tooling takes precedence over conflicting layout preferences, as described in [SKILL.md](../SKILL.md).

License: [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/); the original copyright and license notice is preserved in [LICENSE](../LICENSE). Changes: rules independently restated and shortened, grouped by topic; examples omitted.

Credit: SQL style guide by Simon Holywell is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License. Based on a work at https://www.sqlstyle.guide/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Simon Holywell.

## Original worked examples

See [sources.md](sources.md) for original code, source tags and reading pointers.
