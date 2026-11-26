# Sources and changes

House text: CC-BY-4.0, style-skills contributors. Configurations: MIT (see config/LICENSE).

Changes: independently worded rules combined, conflicts settled, and project-specific scope kept explicit. Source wording and examples are not bundled. Link-only, share-alike, WCAG, and ShellCheck references supply links and attribution only; their licenses do not become the house license.

Related guides and shared rules are included where linked. Local link destinations and config import paths are adjusted for packaging. 

Unofficial: not affiliated with or endorsed by any source owner. NOASSERTION means the license was not established; it is not a reuse grant.

| Source | Owner | Source license | Treatment |
| --- | --- | --- | --- |
| [Effective Rust](https://effective-rust.com/) | David Drysdale; Galloglass Consulting Limited | CC-BY-NC-ND-4.0 | reference-only |
| [Effective Go](https://go.dev/doc/effective_go) | The Go Authors | CC-BY-4.0 | adapt |
| [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments) | The Go Authors and Go Wiki contributors | CC-BY-4.0 | adapt |
| [Google Go Style Guide](https://google.github.io/styleguide/go/) | Google | CC-BY-3.0 | adapt |
| [Uber Go Style Guide](https://github.com/uber-go/guide) | Uber Technologies, Inc. | Apache-2.0 | adapt |
| [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/) | Standard C++ Foundation and its contributors | LicenseRef-CppCoreGuidelines-Internal-Use | reference-only |
| [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) | Google | CC-BY-3.0 | adapt |
| [Google Engineering Practices](https://google.github.io/eng-practices/) | Google | CC-BY-3.0 | reference-only |
| [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) | Conventional Commits contributors | CC-BY-3.0 | reference-only |
| [Semantic Versioning](https://semver.org/) | Tom Preston-Werner and contributors | CC-BY-3.0 | reference-only |
| [Google developer documentation style guide](https://developers.google.com/style) | Google | CC-BY-4.0 | reference-only |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | OWASP Cheat Sheet Series contributors | CC-BY-SA-4.0 | reference-only |
| [Ruff rules](https://docs.astral.sh/ruff/rules/) | Charles Marsh and Astral contributors | MIT | reference-only |
| [golangci-lint docs](https://golangci-lint.run/) | golangci-lint contributors | GPL-3.0-only | reference-only |
| [EditorConfig specification 0.17.2](https://spec.editorconfig.org/) | EditorConfig contributors | CC-BY-3.0 | reference-only |
| [revive v1.17.1 rule descriptions](https://github.com/revive-lint/revive/blob/v1.17.1/RULES_DESCRIPTIONS.md) | revive-lint and project contributors | MIT | reference-only |
| [Go language specification](https://go.dev/ref/spec) | The Go Authors | CC-BY-4.0 | reference-only |
| [Go FAQ: nil errors](https://go.dev/doc/faq#nil_error) | The Go Authors | CC-BY-4.0 | reference-only |
| [Go release history](https://go.dev/doc/devel/release) | The Go Authors | CC-BY-4.0 | reference-only |
| [Go 1.26 modernizers](https://go.dev/doc/go1.26#tools) | The Go Authors | CC-BY-4.0 | reference-only |
| [Go Vulnerability Management](https://go.dev/doc/security/vuln/) | The Go Authors | CC-BY-4.0 | reference-only |
| [log/slog package](https://pkg.go.dev/log/slog) | The Go Authors | BSD-3-Clause | reference-only |
| [context package](https://pkg.go.dev/context) | The Go Authors | BSD-3-Clause | reference-only |
| [testing package](https://pkg.go.dev/testing) | The Go Authors | BSD-3-Clause | reference-only |
| [Ruff TD003](https://docs.astral.sh/ruff/rules/missing-todo-link/) | Charles Marsh and Astral contributors | MIT | reference-only |
| [Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) | OWASP Cheat Sheet Series contributors | CC-BY-SA-4.0 | reference-only |
| [HTTP Headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html) | OWASP Cheat Sheet Series contributors | CC-BY-SA-4.0 | reference-only |
| [Clickjacking Defense](https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html) | OWASP Cheat Sheet Series contributors | CC-BY-SA-4.0 | reference-only |
| [REST Security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#security-headers) | OWASP Cheat Sheet Series contributors | CC-BY-SA-4.0 | reference-only |

## Source tags

| Tag | Reference | Source license |
| --- | --- | --- |
| `[CONVENTIONAL-COMMITS]` | [source 1](https://www.conventionalcommits.org/en/v1.0.0/) | CC-BY-3.0 |
| `[CPP-CORE]` | [source 1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) | LicenseRef-CppCoreGuidelines-Internal-Use |
| `[EDITORCONFIG]` | [source 1](https://spec.editorconfig.org/), [source 2](https://editorconfig.org/) | CC-BY-3.0 |
| `[EFFECTIVE-GO]` | [source 1](https://go.dev/doc/effective_go) | CC-BY-4.0 |
| `[EFFECTIVE-RUST]` | [source 1](https://effective-rust.com/dep-graph.html) | CC-BY-NC-ND-4.0 |
| `[GO-CONTEXT]` | [source 1](https://pkg.go.dev/context) | BSD-3-Clause |
| `[GO-FAQ]` | [source 1](https://go.dev/doc/faq#nil_error) | CC-BY-4.0 |
| `[GO-FIX]` | [source 1](https://go.dev/doc/go1.26#tools), [source 2](https://pkg.go.dev/cmd/go#hdr-Apply_fixes_suggested_by_static_checkers) | CC-BY-4.0 |
| `[GO-RELEASES]` | [source 1](https://go.dev/doc/devel/release) | CC-BY-4.0 |
| `[GO-REVIEW]` | [source 1](https://go.dev/wiki/CodeReviewComments) | CC-BY-4.0 |
| `[GO-SLOG]` | [source 1](https://pkg.go.dev/log/slog) | BSD-3-Clause |
| `[GO-SPEC]` | [source 1](https://go.dev/ref/spec) | CC-BY-4.0 |
| `[GO-TEST]` | [source 1](https://pkg.go.dev/testing), [source 2](https://pkg.go.dev/net/http/httptest), [source 3](https://go.dev/doc/articles/race_detector) | BSD-3-Clause |
| `[GO-VULN]` | [source 1](https://go.dev/doc/security/vuln/) | CC-BY-4.0 |
| `[GOLANGCI]` | [source 1](https://golangci-lint.run/docs/linters/), [source 2](https://github.com/golangci/golangci-lint/blob/v2.15.0/.golangci.reference.yml), [source 3](https://github.com/golangci/golangci-lint/blob/v2.15.0/jsonschema/golangci.jsonschema.json), [source 4](https://golangci-lint.run/docs/configuration/cli/) | GPL-3.0-only |
| `[GOOGLE-DOCS]` | [source 1](https://developers.google.com/style) | CC-BY-4.0 |
| `[GOOGLE-GO]` | [source 1](https://google.github.io/styleguide/go/) | CC-BY-3.0 |
| `[GOOGLE-PYTHON]` | [source 1](https://google.github.io/styleguide/pyguide.html) | CC-BY-3.0 |
| `[GOOGLE-REVIEW]` | [source 1](https://google.github.io/eng-practices/) | CC-BY-3.0 |
| `[OWASP]` | [source 1](https://cheatsheetseries.owasp.org/) | CC-BY-SA-4.0 |
| `[REVIVE]` | [source 1](https://github.com/revive-lint/revive/blob/v1.17.1/RULES_DESCRIPTIONS.md) | MIT |
| `[RUFF]` | [source 1](https://docs.astral.sh/ruff/rules/), [source 2](https://docs.astral.sh/ruff/rules/raise-vanilla-class/), [source 3](https://docs.astral.sh/ruff/rules/blind-except/), [source 4](https://docs.astral.sh/ruff/rules/undocumented-public-method/), [source 5](https://docs.astral.sh/ruff/rules/non-pep695-type-alias/) | MIT |
| `[SEMVER]` | [source 1](https://semver.org/) | CC-BY-3.0 |
| `[UBER-GO]` | [source 1](https://github.com/uber-go/guide/blob/master/style.md) | Apache-2.0 |

## Direct citations

| Page | Source license |
| --- | --- |
| [Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) | CC-BY-SA-4.0 |
| [Clickjacking Defense](https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html) | CC-BY-SA-4.0 |
| [HTTP Headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html) | CC-BY-SA-4.0 |
| [REST Security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#security-headers) | CC-BY-SA-4.0 |
| [Ruff TD003](https://docs.astral.sh/ruff/rules/missing-todo-link/) | MIT |
| [Go 1.26 modernizers](https://go.dev/doc/go1.26#tools) | CC-BY-4.0 |
| [official vulnerability checker](https://go.dev/doc/security/vuln/) | CC-BY-4.0 |
| [slog handlers](https://pkg.go.dev/log/slog) | BSD-3-Clause |

## Attribution notices

- Effective Rust, David Drysdale; Galloglass Consulting Limited, CC-BY-NC-ND-4.0, https://effective-rust.com/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by David Drysdale; Galloglass Consulting Limited.
- Effective Go, The Go Authors, CC-BY-4.0, https://go.dev/doc/effective_go. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by The Go Authors.
- Go Code Review Comments, The Go Authors and Go Wiki contributors, CC-BY-4.0, https://go.dev/wiki/CodeReviewComments. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by The Go Authors and Go Wiki contributors.
- Google Go Style Guide, Google, CC-BY-3.0, https://google.github.io/styleguide/go/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.
- Uber Go Style Guide, Uber Technologies, Inc., Apache-2.0, https://github.com/uber-go/guide. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Uber Technologies, Inc.
- C++ Core Guidelines, Standard C++ Foundation and its contributors, LicenseRef-CppCoreGuidelines-Internal-Use, https://isocpp.github.io/CppCoreGuidelines/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Standard C++ Foundation and its contributors.
- Google Python Style Guide, Google, CC-BY-3.0, https://google.github.io/styleguide/pyguide.html. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.
- Google Engineering Practices, Google, CC-BY-3.0, https://google.github.io/eng-practices/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Google.
- Conventional Commits, Conventional Commits contributors, CC-BY-3.0, https://www.conventionalcommits.org/en/v1.0.0/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Conventional Commits contributors.
- Semantic Versioning, Tom Preston-Werner and contributors, CC-BY-3.0, https://semver.org/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Tom Preston-Werner and contributors.
- Google developer documentation style guide, Google, CC-BY-4.0, https://developers.google.com/style. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Google.
- OWASP Cheat Sheet Series, OWASP Cheat Sheet Series contributors, CC-BY-SA-4.0, https://cheatsheetseries.owasp.org/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by OWASP Cheat Sheet Series contributors.
- Ruff rules, Charles Marsh and Astral contributors, MIT, https://docs.astral.sh/ruff/rules/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Charles Marsh and Astral contributors.
- golangci-lint docs, golangci-lint contributors, GPL-3.0-only, https://golangci-lint.run/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by golangci-lint contributors.
- EditorConfig specification 0.17.2, EditorConfig contributors, CC-BY-3.0, https://spec.editorconfig.org/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by EditorConfig contributors.
- revive v1.17.1 rule descriptions, revive-lint and project contributors, MIT, https://github.com/revive-lint/revive/blob/v1.17.1/RULES_DESCRIPTIONS.md. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by revive-lint and project contributors.
- Go language specification, The Go Authors, CC-BY-4.0, https://go.dev/ref/spec. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by The Go Authors.
- Go FAQ: nil errors, The Go Authors, CC-BY-4.0, https://go.dev/doc/faq#nil_error. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by The Go Authors.
- Go release history, The Go Authors, CC-BY-4.0, https://go.dev/doc/devel/release. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by The Go Authors.
- Go 1.26 modernizers, The Go Authors, CC-BY-4.0, https://go.dev/doc/go1.26#tools. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by The Go Authors.
- Go Vulnerability Management, The Go Authors, CC-BY-4.0, https://go.dev/doc/security/vuln/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by The Go Authors.
- log/slog package, The Go Authors, BSD-3-Clause, https://pkg.go.dev/log/slog. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by The Go Authors.
- context package, The Go Authors, BSD-3-Clause, https://pkg.go.dev/context. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by The Go Authors.
- testing package, The Go Authors, BSD-3-Clause, https://pkg.go.dev/testing. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by The Go Authors.
- Ruff TD003, Charles Marsh and Astral contributors, MIT, https://docs.astral.sh/ruff/rules/missing-todo-link/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Charles Marsh and Astral contributors.
- Authentication, OWASP Cheat Sheet Series contributors, CC-BY-SA-4.0, https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by OWASP Cheat Sheet Series contributors.
- HTTP Headers, OWASP Cheat Sheet Series contributors, CC-BY-SA-4.0, https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by OWASP Cheat Sheet Series contributors.
- Clickjacking Defense, OWASP Cheat Sheet Series contributors, CC-BY-SA-4.0, https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by OWASP Cheat Sheet Series contributors.
- REST Security, OWASP Cheat Sheet Series contributors, CC-BY-SA-4.0, https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#security-headers. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by OWASP Cheat Sheet Series contributors.
