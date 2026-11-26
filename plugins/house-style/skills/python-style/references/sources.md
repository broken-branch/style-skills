# Sources and changes

House text: CC-BY-4.0, style-skills contributors. Configurations: MIT (see config/LICENSE).

Changes: independently worded rules combined, conflicts settled, and project-specific scope kept explicit. Source wording and examples are not bundled. Link-only, share-alike, WCAG, and ShellCheck references supply links and attribution only; their licenses do not become the house license.

Related guides and shared rules are included where linked. Local link destinations and config import paths are adjusted for packaging. 

Unofficial: not affiliated with or endorsed by any source owner. NOASSERTION means the license was not established; it is not a reuse grant.

| Source | Owner | Source license | Treatment |
| --- | --- | --- | --- |
| [Effective Rust](https://effective-rust.com/) | David Drysdale; Galloglass Consulting Limited | CC-BY-NC-ND-4.0 | reference-only |
| [Google Go Style Guide](https://google.github.io/styleguide/go/) | Google | CC-BY-3.0 | adapt |
| [Uber Go Style Guide](https://github.com/uber-go/guide) | Uber Technologies, Inc. | Apache-2.0 | adapt |
| [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/) | Standard C++ Foundation and its contributors | LicenseRef-CppCoreGuidelines-Internal-Use | reference-only |
| [PEP 8](https://peps.python.org/pep-0008/) | Guido van Rossum, Barry Warsaw and Alyssa Coghlan | LicenseRef-Public-Domain-PEP | adapt |
| [PEP 257](https://peps.python.org/pep-0257/) | David Goodger and Guido van Rossum | LicenseRef-Public-Domain-PEP | adapt |
| [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) | Google | CC-BY-3.0 | adapt |
| [Google Engineering Practices](https://google.github.io/eng-practices/) | Google | CC-BY-3.0 | reference-only |
| [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) | Conventional Commits contributors | CC-BY-3.0 | reference-only |
| [Semantic Versioning](https://semver.org/) | Tom Preston-Werner and contributors | CC-BY-3.0 | reference-only |
| [Google developer documentation style guide](https://developers.google.com/style) | Google | CC-BY-4.0 | reference-only |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | OWASP Cheat Sheet Series contributors | CC-BY-SA-4.0 | reference-only |
| [Ruff rules](https://docs.astral.sh/ruff/rules/) | Charles Marsh and Astral contributors | MIT | reference-only |
| [EditorConfig specification 0.17.2](https://spec.editorconfig.org/) | EditorConfig contributors | CC-BY-3.0 | reference-only |
| [Ruff configuration](https://docs.astral.sh/ruff/configuration/) | Charles Marsh and Astral contributors | MIT | reference-only |
| [Ruff formatter](https://docs.astral.sh/ruff/formatter/) | Charles Marsh and Astral contributors | MIT | reference-only |
| [mypy configuration](https://mypy.readthedocs.io/en/stable/config_file.html) | Jukka Lehtosalo and mypy contributors | MIT | reference-only |
| [Python 3.12 typing](https://docs.python.org/3.12/library/typing.html) | Python Software Foundation | PSF-2.0 | reference-only |
| [Python 3.12 coroutines and tasks](https://docs.python.org/3.12/library/asyncio-task.html) | Python Software Foundation | PSF-2.0 | reference-only |
| [Python 3.12 unittest](https://docs.python.org/3.12/library/unittest.html) | Python Software Foundation | PSF-2.0 | reference-only |
| [Python 3.12 security considerations](https://docs.python.org/3.12/library/security_warnings.html) | Python Software Foundation | PSF-2.0 | reference-only |
| [PEP 668: externally managed Python environments](https://peps.python.org/pep-0668/) | PEP 668 authors | CC0-1.0 | reference-only |
| [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) | Charles Marsh and Astral contributors | MIT | reference-only |
| [naive datetimes](https://docs.python.org/3/library/datetime.html#aware-and-naive-objects) | Python Software Foundation | PSF-2.0 | reference-only |
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
| `[EFFECTIVE-RUST]` | [source 1](https://effective-rust.com/dep-graph.html) | CC-BY-NC-ND-4.0 |
| `[GOOGLE-DOCS]` | [source 1](https://developers.google.com/style) | CC-BY-4.0 |
| `[GOOGLE-GO]` | [source 1](https://google.github.io/styleguide/go/) | CC-BY-3.0 |
| `[GOOGLE-PYTHON]` | [source 1](https://google.github.io/styleguide/pyguide.html) | CC-BY-3.0 |
| `[GOOGLE-REVIEW]` | [source 1](https://google.github.io/eng-practices/) | CC-BY-3.0 |
| `[MYPY]` | [source 1](https://mypy.readthedocs.io/en/stable/config_file.html), [source 2](https://mypy.readthedocs.io/en/stable/command_line.html), [source 3](https://mypy.readthedocs.io/en/stable/error_code_list.html), [source 4](https://mypy.readthedocs.io/en/stable/error_code_list2.html) | MIT |
| `[OWASP]` | [source 1](https://cheatsheetseries.owasp.org/) | CC-BY-SA-4.0 |
| `[PEP257]` | [source 1](https://peps.python.org/pep-0257/) | LicenseRef-Public-Domain-PEP |
| `[PEP668]` | [source 1](https://peps.python.org/pep-0668/) | CC0-1.0 |
| `[PEP8]` | [source 1](https://peps.python.org/pep-0008/) | LicenseRef-Public-Domain-PEP |
| `[PY-ASYNCIO]` | [source 1](https://docs.python.org/3.12/library/asyncio-task.html) | PSF-2.0 |
| `[PY-SECURITY]` | [source 1](https://docs.python.org/3.12/library/security_warnings.html) | PSF-2.0 |
| `[PY-TYPING]` | [source 1](https://docs.python.org/3.12/library/typing.html) | PSF-2.0 |
| `[PY-UNITTEST]` | [source 1](https://docs.python.org/3.12/library/unittest.html) | PSF-2.0 |
| `[RUFF]` | [source 1](https://docs.astral.sh/ruff/rules/), [source 2](https://docs.astral.sh/ruff/rules/raise-vanilla-class/), [source 3](https://docs.astral.sh/ruff/rules/blind-except/), [source 4](https://docs.astral.sh/ruff/rules/undocumented-public-method/), [source 5](https://docs.astral.sh/ruff/rules/non-pep695-type-alias/) | MIT |
| `[RUFF-CONFIG]` | [source 1](https://docs.astral.sh/ruff/configuration/), [source 2](https://docs.astral.sh/ruff/settings/) | MIT |
| `[RUFF-FORMAT]` | [source 1](https://docs.astral.sh/ruff/formatter/) | MIT |
| `[SEMVER]` | [source 1](https://semver.org/) | CC-BY-3.0 |
| `[UBER-GO]` | [source 1](https://github.com/uber-go/guide/blob/master/style.md) | Apache-2.0 |
| `[UV]` | [source 1](https://docs.astral.sh/uv/concepts/projects/sync/) | MIT |

## Direct citations

| Page | Source license |
| --- | --- |
| [Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) | CC-BY-SA-4.0 |
| [Clickjacking Defense](https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html) | CC-BY-SA-4.0 |
| [HTTP Headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html) | CC-BY-SA-4.0 |
| [REST Security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#security-headers) | CC-BY-SA-4.0 |
| [Ruff TD003](https://docs.astral.sh/ruff/rules/missing-todo-link/) | MIT |
| [locked project environment](https://docs.astral.sh/uv/concepts/projects/sync/) | MIT |
| [naive datetimes](https://docs.python.org/3/library/datetime.html#aware-and-naive-objects) | PSF-2.0 |
| [PEP 668](https://peps.python.org/pep-0668/) | CC0-1.0 |

## Attribution notices

- Effective Rust, David Drysdale; Galloglass Consulting Limited, CC-BY-NC-ND-4.0, https://effective-rust.com/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by David Drysdale; Galloglass Consulting Limited.
- Google Go Style Guide, Google, CC-BY-3.0, https://google.github.io/styleguide/go/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.
- Uber Go Style Guide, Uber Technologies, Inc., Apache-2.0, https://github.com/uber-go/guide. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Uber Technologies, Inc.
- C++ Core Guidelines, Standard C++ Foundation and its contributors, LicenseRef-CppCoreGuidelines-Internal-Use, https://isocpp.github.io/CppCoreGuidelines/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Standard C++ Foundation and its contributors.
- PEP 8, Guido van Rossum, Barry Warsaw and Alyssa Coghlan, LicenseRef-Public-Domain-PEP, https://peps.python.org/pep-0008/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Guido van Rossum, Barry Warsaw and Alyssa Coghlan.
- PEP 257, David Goodger and Guido van Rossum, LicenseRef-Public-Domain-PEP, https://peps.python.org/pep-0257/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by David Goodger and Guido van Rossum.
- Google Python Style Guide, Google, CC-BY-3.0, https://google.github.io/styleguide/pyguide.html. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.
- Google Engineering Practices, Google, CC-BY-3.0, https://google.github.io/eng-practices/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Google.
- Conventional Commits, Conventional Commits contributors, CC-BY-3.0, https://www.conventionalcommits.org/en/v1.0.0/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Conventional Commits contributors.
- Semantic Versioning, Tom Preston-Werner and contributors, CC-BY-3.0, https://semver.org/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Tom Preston-Werner and contributors.
- Google developer documentation style guide, Google, CC-BY-4.0, https://developers.google.com/style. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Google.
- OWASP Cheat Sheet Series, OWASP Cheat Sheet Series contributors, CC-BY-SA-4.0, https://cheatsheetseries.owasp.org/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by OWASP Cheat Sheet Series contributors.
- Ruff rules, Charles Marsh and Astral contributors, MIT, https://docs.astral.sh/ruff/rules/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Charles Marsh and Astral contributors.
- EditorConfig specification 0.17.2, EditorConfig contributors, CC-BY-3.0, https://spec.editorconfig.org/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by EditorConfig contributors.
- Ruff configuration, Charles Marsh and Astral contributors, MIT, https://docs.astral.sh/ruff/configuration/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Charles Marsh and Astral contributors.
- Ruff formatter, Charles Marsh and Astral contributors, MIT, https://docs.astral.sh/ruff/formatter/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Charles Marsh and Astral contributors.
- mypy configuration, Jukka Lehtosalo and mypy contributors, MIT, https://mypy.readthedocs.io/en/stable/config_file.html. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Jukka Lehtosalo and mypy contributors.
- Python 3.12 typing, Python Software Foundation, PSF-2.0, https://docs.python.org/3.12/library/typing.html. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Python Software Foundation.
- Python 3.12 coroutines and tasks, Python Software Foundation, PSF-2.0, https://docs.python.org/3.12/library/asyncio-task.html. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Python Software Foundation.
- Python 3.12 unittest, Python Software Foundation, PSF-2.0, https://docs.python.org/3.12/library/unittest.html. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Python Software Foundation.
- Python 3.12 security considerations, Python Software Foundation, PSF-2.0, https://docs.python.org/3.12/library/security_warnings.html. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Python Software Foundation.
- PEP 668: externally managed Python environments, PEP 668 authors, CC0-1.0, https://peps.python.org/pep-0668/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by PEP 668 authors.
- uv locking and syncing, Charles Marsh and Astral contributors, MIT, https://docs.astral.sh/uv/concepts/projects/sync/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Charles Marsh and Astral contributors.
- naive datetimes, Python Software Foundation, PSF-2.0, https://docs.python.org/3/library/datetime.html#aware-and-naive-objects. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Python Software Foundation.
- Ruff TD003, Charles Marsh and Astral contributors, MIT, https://docs.astral.sh/ruff/rules/missing-todo-link/. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by Charles Marsh and Astral contributors.
- Authentication, OWASP Cheat Sheet Series contributors, CC-BY-SA-4.0, https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by OWASP Cheat Sheet Series contributors.
- HTTP Headers, OWASP Cheat Sheet Series contributors, CC-BY-SA-4.0, https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by OWASP Cheat Sheet Series contributors.
- Clickjacking Defense, OWASP Cheat Sheet Series contributors, CC-BY-SA-4.0, https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by OWASP Cheat Sheet Series contributors.
- REST Security, OWASP Cheat Sheet Series contributors, CC-BY-SA-4.0, https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#security-headers. Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by OWASP Cheat Sheet Series contributors.
