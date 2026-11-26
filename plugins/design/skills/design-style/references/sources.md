# Sources and changes

House prose and original examples: CC-BY-4.0, style-skills contributors (see the skill's LICENSE). Filtered token configuration: MIT, see [TOKENS-LICENSE](TOKENS-LICENSE). This is an original house system; it is not a company component export. Company palettes, font files, logos, screenshots and source cards are not bundled.

## Evidence boundary

The house design guide and component contracts were reviewed from the 2026-10-31 local snapshot. The public prose is independently written. Original source-tag labels and house adaptation IDs remain below so rules can be traced without publishing private research, identities, links or product vocabulary. Anonymous study IDs identify original visual studies, not public documents.

Shopify informs surface hierarchy and control categories; Notion informs grouped boards and side-detail layout only. Source terms for those company documents were not established by this draft (NOASSERTION); a visual reference is not a redistribution grant. No company sentences, examples, assets or complete palettes are reproduced. Company names record influence and do not imply endorsement. Their online documents were not rechecked for this offline draft.

The house semantic color mapping is retained, including selected values influenced by the surface reference. It is a house adaptation, not an authenticated production theme. New upstream fields or token names require filter review before they can ship.

## Source tags

| Tag retained from house guide | Meaning in this skill |
| --- | --- |
| `Shopify` | Visual surface/control reference; original house wording only; source prose/asset terms unverified. |
| `Notion` | Board grouping, card density and side-detail concepts; no brand color/type adoption; source terms unverified. |
| `mockup-37` | Original warm-sheet/dark-frame study with compact cards and restrained headings. |
| `mockup-32` | Original grouped-board and side-detail layout study. |
| `mockup button rounds` | Button comparison history; glossy treatment excluded, final alternative unselected. |
| `mockup btn-h` | Ownership color concept only; no adoption of the study's control skin. |
| `mockup tall-c` | Original compact top-strip layout study. |
| `mockup square-c` | Original compact rail/split layout study. |
| `house adaptation G01` | Flat action hierarchy and rounded rectangular controls; provisional. |
| `house adaptation G02` | Type roles, readable sizes and generic system font fallback. |
| `house adaptation G03` | Spacing scale, named density exceptions, padding and reading width. |
| `house adaptation G04` | Responsive thresholds, reflow and continued access to details/actions. |
| `house adaptation G05` | Complete warm-neutral dark mapping and explicit/system theme precedence; provisional. |
| `house adaptation G06` | Paired semantic states and stable ownership slots; ownership choice provisional. |
| `house adaptation G07` | Short feedback motion, reduced motion and surface elevations. |
| `house adaptation G08` | Unrounded contrast minima, focus, targets and alternatives to dragging. |
| `house adaptation G09` | Original outline icons and discoverable textual names. |
| `house adaptation G10` | Control states, keyboard behavior, focus management and recoverable updates. Explicit menu/tab/combobox keys and dialog wrap complete this contract in the public draft. |
| `house adaptation G11` | Sentence-case action labels and specific recovery messages. |
| `house adaptation G12` | Portable semantic token schema, color-pair registry and repeatable checks. |
| `[WCAG22]` | [WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/) and [quick reference](https://www.w3.org/WAI/WCAG22/quickref/); criterion numbers and independently worded implementation rules only. |

WCAG 2.2 Recommendation and quick reference, World Wide Web Consortium; LicenseRef-W3C-Document-2023. [Document license](https://www.w3.org/copyright/document-license-2023/). No specification sentences or examples are reproduced; unofficial and not endorsed by World Wide Web Consortium. House thresholds deliberately include large and disabled text and do not claim complete WCAG conformance.

## Filtered token sync

Maintainers run `python3 tools/sync.py` from the repository root with `STYLE_SKILLS_SOURCE` pointing at their source checkout, then `python3 tools/build.py` and `python3 tools/check.py --offline`. The generated sync manifest records both token inputs and the filter profile. Public prose is authored separately and is not overwritten by token sync.

The filter reads only `design/tokens.json` and `design/tokens.css` from the design tree. It replaces metadata, substitutes generic system font stacks, converts the four ownership token prefixes to `color-owner-*`, and drops source CSS comments. It preserves all other accepted token values, pair registries, theme precedence and reduced-motion behavior. It rejects unknown schema/token names, unsafe values, unsupported CSS, JSON/CSS drift, and contrast below 4.5:1 text or 3:1 indicators using unrounded ratios. It never copies design guides, company cards, research or specimen assets.

Change tokens upstream and regenerate their CSS before syncing. New names require a deliberate review of `tools/design-token-profile.json`. Font or metadata edits do not propagate because the public substitutions are intentional. Consuming apps may copy the two bundled files together; their own overrides need a new pair audit and rendered-state checks. CSS media-query literals in examples must track the named JSON breakpoints.
