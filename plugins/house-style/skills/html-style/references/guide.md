# HTML style guide

Scope: authored HTML Living Standard documents served as `text/html`, including assembled server-rendered pages and browser-rendered output; accessibility targets WCAG 2.2 Level AA (all applicable A and AA criteria). JSX, Vue templates, email HTML, XHTML, and third-party/generated source need their own parsing profiles. The rendered web experience still needs accessibility evaluation.
Baseline: [shared rules](shared.md), including dependencies, commits, versioning, review, and AI agent workflow.
MUST means required; PREFER means the default, with a reason recorded for departures.
Source tags resolve in [source credits](sources.md#source-tags).

## Quick rules

- MUST run axe-core through Playwright and scripted keyboard navigation on changed rendered pages/states, reporting violations and checks that could not run. Why: automated browser checks catch defects beyond static markup while leaving human release gates explicit. [MDN-A11Y] [Playwright accessibility](https://playwright.dev/docs/accessibility-testing)
- MUST give each full HTML document an HTML doctype, explicit html/head/body elements, a meaningful title, a primary `lang`, UTF-8 charset metadata first in head, and viewport metadata that allows zoom. Why: browsers and assistive technology need a predictable document entry point. [LEARN-HTML] [WCAG22]
- MUST explicitly close non-void HTML elements, including paragraphs and list items with optional end tags. Why: authored source should make the intended DOM boundaries visible. [LEARN-HTML] [GOOGLE-DOCS]
- MUST choose semantic HTML for the actual content: headings, paragraphs, lists, navigation, and table cells carry meaning rather than merely presentation. Why: structure must be programmatically available (1.3.1). [WCAG22] [LEARN-HTML]
- MUST use one visible main landmark and one page h1, with descriptive headings that increase by at most one rank when entering a subsection. Why: one explicit hierarchy makes navigation predictable; the exact h1/rank convention is house policy supporting 1.3.1 and 2.4.6. [LEARN-HTML] [WCAG22]
- MUST provide a keyboard-reachable skip link to main content on pages with repeated navigation, visible when focused. Why: repeated blocks must be bypassable (2.4.1). [LEARN-HTML] [WCAG22]
- MUST give authored IDs unique lowercase names beginning with a letter and containing hyphen-separated nonempty words or numeric segments, with at least one hyphen. Why: a predictable subset avoids selector escaping and bare JavaScript-identifier collisions. [GOOGLE-HTMLCSS] [LEARN-HTML]
- MUST use buttons with explicit types for actions and anchors with real destinations for navigation. Why: native semantics provide the expected activation, keyboard behavior, and form-submission intent. [MDN-A11Y] [HTML-VALIDATE]
- MUST give every user-entry control an associated visible label and group related controls with fieldset/legend where a group label is needed. Why: instructions and relationships must be available visually and programmatically (1.3.1, 3.3.2). [WCAG22] [LEARN-HTML]
- MUST give inputs explicit suitable types, submitted fields appropriate names, and recognized personal-data fields accurate autocomplete tokens. Why: input semantics improve validation, virtual keyboards, and purpose identification (1.3.5). [LEARN-HTML] [WCAG22]
- MUST omit false HTML Boolean attributes instead of writing values such as `disabled="false"`; use the specified string values for enumerated and ARIA attributes. Why: Boolean presence means true, while ARIA and enumerated attributes have different value models. [HTML-STANDARD]
- MUST give meaningful images context-appropriate alt text, use `alt=""` for purely decorative or redundant images, and provide an equivalent explanation for complex graphics. Why: nontext information needs an accessible equivalent (1.1.1). [WCAG22] [LEARN-HTML]
- MUST reserve tables for tabular data, provide a caption or equivalent name, and associate headers with cells using appropriate scope or explicit headers/ID relationships. Why: data relationships must survive nonvisual reading (1.3.1). [WCAG22] [LEARN-HTML]
- MUST provide prerecorded audio-only transcripts and video-only text/audio alternatives, prerecorded synchronized captions, live synchronized captions, and audio description for prerecorded synchronized video where 1.2.1–1.2.5 require them. Why: WCAG A/AA media access is required even when alternatives are not already available. [WCAG22]
- MUST keep all controls keyboard-operable with meaningful DOM/focus order, visible focus that author content does not entirely obscure, and a way to leave each component. Why: keyboard users need reachable, perceivable, escapable interaction (2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11). [WCAG22]
- MUST use only `tabindex="0"` for ordinary added tab stops or `tabindex="-1"` for programmatic focus, and leave native controls' tabindex unset unless necessary. Why: positive tabindex creates a competing focus order. [LEARN-HTML] [MDN-A11Y]
- MUST hide inactive content with an appropriate hidden/removal mechanism, or make visible inactive regions inert; never leave focusable content inside aria-hidden subtrees. Why: aria-hidden changes accessibility exposure without preventing interaction. [MDN-ARIA-HIDDEN] [MDN-A11Y]
- MUST use native element semantics where they fit and add ARIA only for missing semantics, maintaining every custom control's name, role, state, keyboard behavior, and focus management. Why: ARIA describes a widget but does not implement it (4.1.2). [WCAG22] [LEARN-HTML]
- MUST identify invalid fields and describe errors in text, associate explanations with their controls, and suggest known corrections unless security or purpose forbids them. Why: errors must be identifiable and repairable without color alone (3.3.1, 3.3.3). [WCAG22] [LEARN-HTML]
- MUST require deliberate user activation before audio/video or nonessential animated imagery starts, and provide controls to pause or stop it. Why: opt-in motion is the house default beyond WCAG AA's conditional autoplay limits. [MDN-A11Y] [LEARN-HTML] [WCAG22]
- MUST test pointer targets at 24 by 24 CSS pixels or a qualifying spacing/equivalent-control exception, and provide nondragging single-pointer alternatives unless dragging is essential or unmodified native behavior. Why: WCAG 2.2 AA adds target-size and dragging requirements (2.5.7, 2.5.8). [WCAG22]
- MUST verify authentication works with password managers and paste, and avoid mandatory cognitive tests without a qualifying alternative, assistance, or exception. Why: accessible authentication must not depend only on memory or puzzle solving (3.3.8). [WCAG22]
- MUST render untrusted plain text with template autoescaping or `textContent`, and use a reviewed HTML sanitizer when rich markup is intentionally accepted. Why: HTML parsing sinks such as innerHTML turn unescaped data into active markup. [OWASP]
- MUST require human keyboard and supported-screen-reader checks before release, covering labels, headings, tables, dialogs, errors, and updates; agents report unperformed checks as pending. Why: scripts cannot establish the complete assistive-technology experience. [MDN-A11Y] [WCAG22]
- PREFER link labels that identify their destination or action when read alone; always make purpose clear from text or programmatically associated context. Why: standalone labels aid link lists while the mandatory floor is WCAG 2.4.4. [MDN-A11Y] [GOOGLE-DOCS] [WCAG22]

## Tooling

For your project, copy the bundled HTML Validate profiles and root Prettier config, then run `html-validate --config .htmlvalidate.json path/to/your-page.html` and `prettier --config .prettierrc.json --check path/to/your-page.html`, replacing the example input with your own authored or assembled HTML files.

| Purpose | Tool and version | Config file | Repository command |
| --- | --- | --- | --- |
| Formatter | Prettier 3.9.10 | [Root web `.prettierrc.json`](config/.prettierrc.json) | `npx prettier --check .` |
| Linter | HTML Validate 11.17.0 | [`.htmlvalidate.json`](config/.htmlvalidate.json); explicit rules, HTML5 metadata | `npx html-validate --config .htmlvalidate.json <built-html-files>` |
| Build / type checks | Not applicable to plain HTML | Template/compiler checks belong to the consuming application | Not applicable |
| Tests | @playwright/test 1.64.1 + @axe-core/playwright 4.14.0; human release checks below | Project's Playwright configuration and tests against its own pages | Project's browser and accessibility test command |

Mechanical formatting: the formatter handles this. Copy [the single web config](config/.prettierrc.json) to the consuming repository root as `.prettierrc.json`; do not add competing language configs. TypeScript/TSX and Vue scripts use `singleQuote: true`; standalone `*.css` uses `false`. Vue `<style>` uses the SFC's `true` setting too. Only `*.html` disables embedded-language formatting; Vue scripts/styles remain formatted. [PRETTIER]

Run the commands from the project root after adopting the HTML Validate profiles and shared Prettier config, pinning the listed tools, and selecting the project’s authored or assembled HTML files. `root: true`, `extends: []`, and explicit rules prevent unintended config inheritance. [HTML-VALIDATE] [PRETTIER]

Prettier 3.9.10 and HTML Validate 11.17.0 passed on sample documents. Full browser, axe, keyboard, and screen-reader validation remains required on the consuming application; no complete accessibility pass is claimed.

- MUST validate complete assembled HTML documents with this profile, including states produced by templates; use framework-aware tooling for template source. Why: IDs, references, headings, and document requirements depend on the combined output. [HTML-VALIDATE]
- MUST describe real custom elements in HTML Validate metadata before validating documents containing them. Why: unknown elements otherwise bypass meaningful content-model checks or fail the selected rule. [HTML-VALIDATE]
- MUST require human evaluation of rendered pages and complete user processes against every applicable WCAG 2.2 A and AA success criterion before release; agents report that gate as pending until evidence is supplied. Why: automated checks cannot establish full accessibility conformance. [WCAG22]

### Rendered-output validation

Authored IDs retain the naming rule. For assembled framework output containing generated IDs such as React `useId`, use [`.htmlvalidate-rendered.json`](config/.htmlvalidate-rendered.json): it extends the authored profile, disables only `id-pattern`, and sets `valid-id: { relaxed: true }`. Nonempty/whitespace-free IDs, `no-dup-id`, `valid-for`, and `no-missing-references` remain errors. Authored naming still needs source-level checking/review when generated and authored IDs coexist. [HTML Validate valid-id](https://html-validate.org/rules/valid-id.html) [REACT-ID]

```sh
npx html-validate --config .htmlvalidate-rendered.json <built-html-files>
```

Validate complete rendered documents, including generated IDs and label/description references; this is not a JSX or template-source parser. [REACT-ID]

### Config enforcement by rule ID

Every enabled rule is listed below, all at error severity. The descriptions identify the check's reach, not a promise that every defect in that category is detected. `wcag/h*` IDs name selected HTML techniques; WCAG permits other sufficient techniques and does not mandate this linter. [HTML-VALIDATE] [WCAG22]

| Rule ID | Configured check |
| --- | --- |
| `area-alt` | Alternative text on linked image-map areas. |
| `aria-hidden-body` | No accessibility-tree hiding of the entire body. |
| `aria-label-misuse` | Naming attributes used on elements that support names. |
| `attr-spacing` | Attribute separation required by HTML syntax. |
| `attribute-allowed-values` | Metadata-defined values; Boolean validity and the custom tabindex/lang restrictions below. |
| `attribute-misuse` | Attribute dependencies and incompatible combinations. |
| `autocomplete-password` | Password controls have autocomplete and do not use `off`; purpose still needs review. |
| `close-attr` | No attributes on closing tags. |
| `close-order` | Correct element closure/nesting. |
| `deprecated` | Obsolete elements recognized by metadata. |
| `doctype-html` | HTML doctype when present. |
| `element-name` | Native or syntactically valid custom-element names. |
| `element-permitted-content` | Permitted children/descendants from metadata. |
| `element-permitted-occurrences` | Permitted counts of particular child elements. |
| `element-permitted-order` | Required child order. |
| `element-permitted-parent` | Permitted immediate parents. |
| `element-required-ancestor` | Required ancestor contexts. |
| `element-required-attributes` | Required attributes, including the profile's `html[lang]` and `img[alt]`. |
| `element-required-content` | Required children, including explicit head/body under html and title under head. |
| `empty-heading` | Nonempty headings; does not judge descriptive quality. |
| `empty-title` | Nonempty page title; does not compare titles across pages. |
| `form-dup-name` | Accidental shared control names; radio/checkbox groups and submit/button/reset same-type groups explicitly allowed; default array-bracket and hidden-checkbox allowances retained. |
| `heading-level` | First heading h1, no downward rank skips, at most one h1; `sectioningRoots: []` applies one outline including dialogs. |
| `hidden-focusable` | Statically detected focusable content under aria-hidden; negative-tabindex/programmatic focus still needs review. |
| `id-pattern` | Authored IDs match `^[a-z][a-z0-9]*(-[a-z0-9]+)+$`: lowercase, letter first, at least one hyphen. |
| `input-attributes` | Attributes appropriate to the input type. |
| `input-missing-label` | Input/select/textarea accessible naming; also accepts ARIA-only names, so visible labels need review. |
| `map-dup-name` | Unique image-map names. |
| `map-id-name` | Matching name/id on image maps. |
| `meta-refresh` | Rejects delayed meta refresh; does not prohibit immediate redirects. |
| `missing-doctype` | Document has a doctype. |
| `multiple-labeled-controls` | One label does not identify multiple controls. |
| `no-abstract-role` | No abstract ARIA roles. |
| `no-autoplay` | No autoplay attribute on audio/video; does not inspect script playback or animated assets. |
| `no-conditional-comment` | No obsolete browser conditional comments. |
| `no-deprecated-attr` | Obsolete attributes recognized by metadata. |
| `no-dup-attr` | No repeated attributes on one element. |
| `no-dup-class` | No repeated class tokens on one element. |
| `no-dup-id` | Unique IDs within the checked document. |
| `no-implicit-button-type` | Explicit button type. |
| `no-implicit-close` | Explicit closure of elements with optional end tags. |
| `no-implicit-input-type` | Explicit input type. |
| `no-missing-references` | Existing label-for, input-list, and supported ARIA ID references; not URL-fragment or table-headers validation. |
| `no-multiple-main` | Rejects multiple non-hidden main elements. |
| `no-raw-characters` | Detects unescaped syntax-significant characters. |
| `no-redundant-role` | Rejects repeated implicit roles except `list`, retained for evidenced browser/AT workarounds. |
| `no-unknown-elements` | Elements require metadata; custom elements are not silently accepted. |
| `prefer-native-element` | Known ARIA-role substitutions use native equivalents. |
| `script-element` | Script elements have end tags. |
| `script-type` | Rejects redundant classic JavaScript MIME types; module/data-block types remain possible. |
| `text-content` | Metadata-required accessible text, notably button names. |
| `unique-landmark` | Repeated landmarks of a type have distinct names; stricter than some valid repeated-navigation patterns. |
| `unrecognized-char-ref` | Recognized character references. |
| `valid-autocomplete` | Supported autocomplete tokens, ordering, and control-type compatibility. |
| `valid-for` | Labels reference labelable controls. |
| `valid-id` | Nonempty, whitespace-free IDs with the default identifier restrictions. |
| `void-content` | Void elements have no content/end tags. |
| `wcag/h30` | Links have accessible text, including image alternatives. |
| `wcag/h32` | Forms contain or reference a submit control. |
| `wcag/h36` | Image submit controls have alternatives. |
| `wcag/h37` | Image alternatives, accepting empty/hidden cases; the added metadata separately requires alt on every img. |
| `wcag/h67` | Empty-alt images do not have nonempty title tooltips. |
| `wcag/h71` | Fieldsets have a legend as their first child element; wording needs review. |

Inline metadata adds `html.lang.required`, a non-whitespace check for its value, `html.requiredContent`, `head.requiredContent`, `img.alt.required`, and global `tabindex.enum: ["-1", "0"]`. It does not validate BCP 47 language tags, require every missing document-root element, check charset placement, or inspect CSS/computed focusability. The HTML5 metadata remains the base. [HTML-VALIDATE]

The root Prettier config supplies the shared TypeScript options. Its `*.html` override supplies `htmlWhitespaceSensitivity`, `singleAttributePerLine`, and `embeddedLanguageFormatting: off`; embedded script/style formatting is off only for HTML so their own tools handle those languages. Whitespace sensitivity stays `css` because inline spacing can affect text. [PRETTIER]

### Deliberate limits and review duties

The explicit profile leaves `wcag/h63` unset because its scope requirement can reject valid complex tables using `headers`/`id`; table associations require review. `no-unknown-attributes` is still documented as experimental and is not selected. Inline styles/style tags are preferences, so their blanket bans are not enabled. Quote, wrapping, Boolean-spelling, void-slash, and whitespace-style rules remain formatter-owned. [HTML-VALIDATE]

HTML lint does not prove alternative-text quality, label-in-name, visible labels, media captions/descriptions, link purpose, keyboard behavior, focus management, contrast, zoom/reflow, target size, accessible authentication, or sanitization. The presence of a fieldset legend does not prove all related controls were grouped. The Testing section covers these boundaries. [WCAG22] [HTML-VALIDATE]

## Naming

- MUST give authored IDs unique lowercase names beginning with a letter and containing hyphen-separated nonempty words or numeric segments, with at least one hyphen. Why: a predictable subset avoids selector escaping and bare JavaScript-identifier collisions. [GOOGLE-HTMLCSS] [LEARN-HTML]
- PREFER classes for styling and `data-*` attributes for script hooks; reserve IDs for fragments, labels, and other real references. Why: unnecessary global identifiers couple unrelated consumers. [GOOGLE-HTMLCSS]
- PREFER lowercase hyphen-separated class names that describe the element's purpose rather than its current appearance. Why: markup hooks survive visual redesigns. [GOOGLE-HTMLCSS]
- MUST give each interactive control an accessible name containing its visible label text, and label repeated landmark types distinctly. Why: voice control and landmark navigation need predictable names (2.5.3, 4.1.2); distinct repeated-landmark names are a house convention. [WCAG22] [MDN-A11Y] [HTML-VALIDATE]
- PREFER link labels that identify their destination or action when read alone; always make purpose clear from text or programmatically associated context. Why: standalone labels aid link lists while the mandatory floor is WCAG 2.4.4. [MDN-A11Y] [GOOGLE-DOCS] [WCAG22]

## Files and layout

- MUST give each full HTML document an HTML doctype, explicit html/head/body elements, a meaningful title, a primary `lang`, UTF-8 charset metadata first in head, and viewport metadata that allows zoom. Why: browsers and assistive technology need a predictable document entry point. [LEARN-HTML] [WCAG22]
- MUST explicitly close non-void HTML elements, including paragraphs and list items with optional end tags. Why: authored source should make the intended DOM boundaries visible. [LEARN-HTML] [GOOGLE-DOCS]
- MUST choose semantic HTML for the actual content: headings, paragraphs, lists, navigation, and table cells carry meaning rather than merely presentation. Why: structure must be programmatically available (1.3.1). [WCAG22] [LEARN-HTML]
- MUST use one visible main landmark and one page h1, with descriptive headings that increase by at most one rank when entering a subsection. Why: one explicit hierarchy makes navigation predictable; the exact h1/rank convention is house policy supporting 1.3.1 and 2.4.6. [LEARN-HTML] [WCAG22]
- MUST provide a keyboard-reachable skip link to main content on pages with repeated navigation, visible when focused. Why: repeated blocks must be bypassable (2.4.1). [LEARN-HTML] [WCAG22]
- MUST mark meaningful changes of human language with `lang`, excluding proper names, technical terms, and assimilated words where WCAG permits. Why: pronunciation follows the passage's language (3.1.2). [WCAG22]
- PREFER linked stylesheets and external scripts to inline presentation and behavior. Why: structural markup stays readable and shared resources can be cached. [GOOGLE-HTMLCSS] [LEARN-HTML]
- MUST retain equivalent repeated navigation, control identification, and help mechanisms in consistent relative positions across related pages. Why: users should not have to relearn each page (3.2.3, 3.2.4, 3.2.6). [WCAG22]
- MUST provide more than one way to locate pages within a set, except process steps/results. Why: different navigation strategies must reach the same content (2.4.5). [WCAG22]

## Types and data

- MUST omit false HTML Boolean attributes instead of writing values such as `disabled="false"`; use the specified string values for enumerated and ARIA attributes. Why: Boolean presence means true, while ARIA and enumerated attributes have different value models. [HTML-STANDARD]
- MUST use buttons with explicit types for actions and anchors with real destinations for navigation. Why: native semantics provide the expected activation, keyboard behavior, and form-submission intent. [MDN-A11Y] [HTML-VALIDATE]
- MUST give every user-entry control an associated visible label and group related controls with fieldset/legend where a group label is needed. Why: instructions and relationships must be available visually and programmatically (1.3.1, 3.3.2). [WCAG22] [LEARN-HTML]
- MUST give inputs explicit suitable types, submitted fields appropriate names, and recognized personal-data fields accurate autocomplete tokens. Why: input semantics improve validation, virtual keyboards, and purpose identification (1.3.5). [LEARN-HTML] [WCAG22]
- MUST use distinct form-control names except deliberate shared-value groups or array contracts, with matching radio names only within the intended group. Why: browser selection and submitted field multiplicity depend on names. [LEARN-HTML] [HTML-VALIDATE]
- MUST provide an explicit submit control for each form and avoid unexpected context changes on focus or input changes. Why: users need deliberate submission and predictable interaction (3.2.1, 3.2.2). [WCAG22] [HTML-VALIDATE]
- MUST give meaningful images context-appropriate alt text, use `alt=""` for purely decorative or redundant images, and provide an equivalent explanation for complex graphics. Why: nontext information needs an accessible equivalent (1.1.1). [WCAG22] [LEARN-HTML]
- MUST use actual text instead of images of text when the technology supports the presentation, except essential presentations such as logos or user-customizable text images. Why: the AA criterion preserves resizing and personalization while retaining its stated exceptions (1.4.5). [WCAG22]
- MUST reserve tables for tabular data, provide a caption or equivalent name, and associate headers with cells using appropriate scope or explicit headers/ID relationships. Why: data relationships must survive nonvisual reading (1.3.1). [WCAG22] [LEARN-HTML]
- MUST provide prerecorded audio-only transcripts and video-only text/audio alternatives, prerecorded synchronized captions, live synchronized captions, and audio description for prerecorded synchronized video where 1.2.1–1.2.5 require them. Why: WCAG A/AA media access is required even when alternatives are not already available. [WCAG22]
- MUST include relevant sounds in captions and distinguish captions from translated subtitles; link transcripts outside the media fallback subtree. Why: equivalent information must remain available even when the browser supports playback. [WCAG22] [MDN-A11Y] [LEARN-HTML]
- PREFER native audio/video controls, replacing them only after a keyboard-accessible alternative works in supported browsers and assistive technology. Why: a custom player assumes responsibility for playback, focus, and state exposure. [LEARN-HTML] [MDN-A11Y]

For media, the labeled-alternative-to-text exceptions in 1.2.1–1.2.3 remain available; 1.2.4 concerns live synchronized audio, and 1.2.5 requires prerecorded synchronized video description at AA. A transcript alone does not replace 1.2.5 audio description; footage already fully described by its soundtrack needs no redundant description track. [WCAG22]

## Errors

- MUST identify invalid fields and describe errors in text, associate explanations with their controls, and suggest known corrections unless security or purpose forbids them. Why: errors must be identifiable and repairable without color alone (3.3.1, 3.3.3). [WCAG22] [LEARN-HTML]
- MUST mark invalid controls with `aria-invalid` after validation, connect help/errors with `aria-describedby` or an appropriately supported error association, and clear stale custom validity messages after correction. Why: the displayed and programmatic validation state must agree. [LEARN-HTML] [MDN-A11Y]
- MUST expose status updates through an appropriate status/live-region mechanism without moving focus merely to announce them. Why: assistive technology needs non-disruptive feedback (4.1.3). [WCAG22]
- MUST offer reversal, error checking with correction, or review and confirmation for consequential submissions covered by 3.3.4. Why: commitments, transactions, stored-data changes, and test answers need an error-prevention path. [WCAG22]
- MUST avoid asking users to reenter information already provided in the same process unless an essential, security, or validity exception applies. Why: redundant entry creates avoidable cognitive and physical effort (3.3.7). [WCAG22]

## Comments and docs

- MUST encode markup examples displayed inside pre/code as text rather than inserting executable tags. Why: the example must display its source instead of altering the page. [GOOGLE-HTMLCSS]
- PREFER visible explanatory content and table captions over essential instructions stored only in title tooltips or comments. Why: hover-only and source-only information is unavailable to many readers. [MDN-A11Y] [LEARN-HTML]

## Testing

- MUST run axe-core through Playwright and scripted keyboard navigation on changed rendered pages/states, reporting violations and checks that could not run. Why: automated browser checks catch defects beyond static markup while leaving human release gates explicit. [MDN-A11Y] [Playwright accessibility](https://playwright.dev/docs/accessibility-testing)
- MUST require human keyboard and supported-screen-reader checks before release, covering labels, headings, tables, dialogs, errors, and updates; agents report unperformed checks as pending. Why: scripts cannot establish the complete assistive-technology experience. [MDN-A11Y] [WCAG22]
- MUST verify 200% text resizing, 320-CSS-pixel-width reflow (or 256-pixel-height for vertical writing), and WCAG text-spacing overrides without lost content or operation, respecting criterion-specific exceptions. Why: responsive styling must preserve access at increased magnification (1.4.4, 1.4.10, 1.4.12). [WCAG22]
- MUST test text contrast at 4.5:1, or 3:1 for large text, and required component/graphic contrast at 3:1, applying only the defined exceptions. Why: readable content and identifiable controls need measurable contrast (1.4.3, 1.4.11). [WCAG22]
- MUST test pointer targets at 24 by 24 CSS pixels or a qualifying spacing/equivalent-control exception, and provide nondragging single-pointer alternatives unless dragging is essential or unmodified native behavior. Why: WCAG 2.2 AA adds target-size and dragging requirements (2.5.7, 2.5.8). [WCAG22]
- MUST verify authentication works with password managers and paste, and avoid mandatory cognitive tests without a qualifying alternative, assistance, or exception. Why: accessible authentication must not depend only on memory or puzzle solving (3.3.8). [WCAG22]
- MUST test actual media playback, caption accuracy/synchronization, description coverage, and pause controls. Why: the presence of track or controls markup does not prove accessible media. [WCAG22] [MDN-A11Y]

Pin @playwright/test 1.64.1 and @axe-core/playwright 4.14.0 with matching browser binaries in the consuming application's lockfile. Use its real pages and meaningful states to test applicable WCAG A/AA axe tags, keyboard navigation, skip links, radio groups, and disclosures. Automated checks supplement the human checks below.

Review axe `incomplete` results as manual follow-ups; a zero-violation scan is not WCAG conformance. Human release evidence must name tested flows, browser/assistive-technology combinations, results, and remaining failures; agents report it as pending when unavailable.

Large text for 1.4.3 means at least 18 points, or 14 points bold. The 1.4.12 override test uses line height 1.5 times font size, paragraph spacing 2 times font size, letter spacing 0.12 times font size, and word spacing 0.16 times font size; these are test settings, not mandatory CSS defaults. Target spacing under 2.5.8 uses nonintersecting 24-pixel circles centered on undersized targets; inline, equivalent, native, and essential-presentation exceptions have specific conditions. [WCAG22]

## Performance

- MUST reserve the intended aspect ratio for images/video with appropriate dimensions and preserve it during responsive sizing. Why: media loading should not shift surrounding content. [LEARN-HTML]
- PREFER responsive image sources with accurate sizes when using width descriptors. Why: the browser can select an image suited to the rendered size. [LEARN-HTML]
- PREFER native details/summary for simple disclosures and native controls for ordinary interactions. Why: built-in behavior avoids unnecessary script and initialization work. [LEARN-HTML]

## Security

- MUST use HTTPS for deployed page resources and form destinations; never fall back to HTTP inside an authenticated page. Why: mixed-content or insecure submission breaks the transport boundary. [GOOGLE-HTMLCSS] [OWASP]
- MUST use POST over HTTPS for sensitive form submissions rather than putting sensitive values into GET URLs. Why: URLs propagate into history, referrers, and logs; POST alone does not encrypt data. [LEARN-HTML] [OWASP]
- MUST render untrusted plain text with template autoescaping or `textContent`, and use a reviewed HTML sanitizer when rich markup is intentionally accepted. Why: HTML parsing sinks such as innerHTML turn unescaped data into active markup. [OWASP]
- MUST constrain untrusted URL schemes before placing them in href/src/action, and avoid interpolating data into inline event handlers or script bodies. Why: HTML escaping alone does not make URL or executable contexts safe. [OWASP]
- MUST treat hidden/disabled controls, client constraint validation, and robots metadata as user-interface behavior rather than server-side authorization. Why: callers can alter or bypass every client-controlled value. [LEARN-HTML] [OWASP]

## Language-specific pitfalls

- MUST keep all controls keyboard-operable with meaningful DOM/focus order, visible focus that author content does not entirely obscure, and a way to leave each component. Why: keyboard users need reachable, perceivable, escapable interaction (2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11). [WCAG22]
- MUST use only `tabindex="0"` for ordinary added tab stops or `tabindex="-1"` for programmatic focus, and leave native controls' tabindex unset unless necessary. Why: positive tabindex creates a competing focus order. [LEARN-HTML] [MDN-A11Y]
- MUST hide inactive content with an appropriate hidden/removal mechanism, or make visible inactive regions inert; never leave focusable content inside aria-hidden subtrees. Why: aria-hidden changes accessibility exposure without preventing interaction. [MDN-ARIA-HIDDEN] [MDN-A11Y]
- MUST use native element semantics where they fit and add ARIA only for missing semantics, maintaining every custom control's name, role, state, keyboard behavior, and focus management. Why: ARIA describes a widget but does not implement it (4.1.2). [WCAG22] [LEARN-HTML]
- MUST omit redundant roles except an evidenced compatibility workaround, such as list semantics lost by a browser/AT combination after list-style removal. Why: unnecessary ARIA can obscure the native contract. [LEARN-HTML] [MDN-A11Y]
- MUST avoid nesting interactive controls such as a button inside a link, and put nested lists inside list items. Why: invalid content models produce ambiguous activation or repaired DOM trees. [LEARN-HTML]
- MUST require deliberate user activation before audio/video or nonessential animated imagery starts, and provide controls to pause or stop it. Why: opt-in motion is the house default beyond WCAG AA's conditional autoplay limits. [MDN-A11Y] [LEARN-HTML] [WCAG22]
- MUST keep flashing within 2.3.1's frequency/area thresholds and make nonessential moving or automatically updating content pausable, stoppable, hideable, or rate-controllable as 2.2.2 requires. Why: media activation alone does not remove seizure or distraction risks. [WCAG22]
- MUST respect `prefers-reduced-motion` for nonessential motion and preserve the underlying interaction when motion is removed. Why: motion must remain controllable (house choice beyond AA; WCAG 2.3.3 is AAA). [WEBDEV-CSS] [WCAG22]
- MUST let users turn off, adjust, or repeatedly extend content-set time limits under 2.2.1 unless a defined exception applies. Why: real-time, essential, and very long limits have narrow exceptions rather than a general timeout exemption. [WCAG22]
- MUST make custom hover/focus content dismissible where required, hoverable, and persistent; provide noncolor cues and avoid sensory-only instructions. Why: users need time and alternative ways to perceive information (1.4.13, 1.4.1, 1.3.3). [WCAG22]
- MUST provide accessible alternatives to multipoint/path gestures and device-motion actions, allow pointer cancellation as specified, and make character-key shortcuts disableable, remappable, or focus-scoped. Why: alternate input methods must operate the interface (2.5.1, 2.5.2, 2.5.4, 2.1.4). [WCAG22]
- MUST allow portrait and landscape use unless orientation is essential, and preserve user zoom. Why: viewport and orientation restrictions can block magnification and fixed-device use (1.3.4, 1.4.4). [WCAG22] [LEARN-HTML]
- MUST give dialogs accessible names, choose initial focus deliberately, and restore focus appropriately when they close. Why: modal transitions must preserve context and keyboard navigation. [LEARN-HTML] [WCAG22]
- MUST keep type="module" on module scripts and necessary types on non-JavaScript data blocks while omitting redundant classic-JavaScript/CSS MIME types. Why: removing a meaningful type changes execution rather than merely simplifying markup. [GOOGLE-HTMLCSS] [HTML-VALIDATE]
- MUST maintain valid HTML even though WCAG 2.2 removed Parsing 4.1.1. Why: browser repair can still break semantics, labels, and interaction under other criteria. [GOOGLE-HTMLCSS] [WCAG22]

## Where the sources disagree

Where the sources disagree, the following house choices apply. Each choice states the adopted behavior and its reason.

- MUST include optional document elements and explicitly close non-void elements: Google's general guide permits omission, Learn HTML recommends closing paragraphs/lists, and Google's documentation guide requires optional elements in documentation. Why: the house extends explicit structure to authored HTML generally for predictable review and checking. [GOOGLE-HTMLCSS] [LEARN-HTML] [GOOGLE-DOCS]
- MUST use letter-led lowercase hyphenated authored IDs with at least one hyphen: Google's required hyphen narrows Learn HTML's broader permitted convention. Why: their compatible intersection gives the validator one concrete naming rule. [GOOGLE-HTMLCSS] [LEARN-HTML]
- MUST apply WCAG 1.4.5's AA essential/customizable exceptions for images of text, rather than turning MDN's categorical tutorial warning into an exceptionless prohibition. Why: the declared target is AA, with real text as the normal implementation. [MDN-A11Y] [WCAG22]
- MUST provide the media alternatives required by WCAG 1.2.1–1.2.5, despite Google's availability-qualified captions/transcripts advice. Why: lack of an existing asset is not a WCAG exception. [GOOGLE-HTMLCSS] [WCAG22]
- MUST use HTTPS for deployed resources, rejecting Google's HTTP fallback when it would conflict with OWASP's encrypted-session and no-mixed-content requirements. Why: one secure production transport rule prevents unsafe fallback. [GOOGLE-HTMLCSS] [OWASP]
- PREFER standalone meaningful link labels as MDN and Google documentation recommend, while requiring at least WCAG 2.4.4's programmatic context instead of claiming AAA 2.4.9 is mandatory at AA. Why: the stronger default helps navigation without misrepresenting the conformance level. [MDN-A11Y] [GOOGLE-DOCS] [WCAG22]
- MUST require activation before media/nonessential animated imagery starts, following MDN's opt-in guidance over Learn HTML's controlled decorative-autoplay allowance. Why: a stricter house default prevents surprise motion and gives no-autoplay a clear policy basis. [MDN-A11Y] [LEARN-HTML] [WCAG22]
- MUST hide or inert inactive regions instead of using aria-hidden alone, choosing MDN's mobile checklist and current attribute reference over the older widget article's visibility synchronization shortcut. Why: accessibility hiding does not remove keyboard focusability. [MDN-A11Y] [MDN-ARIA-HIDDEN]
- PREFER native media controls with testing, following Learn HTML's baseline over MDN's older blanket keyboard-limitations claim; replace controls only for demonstrated target-browser needs. Why: source age cannot establish actual browser/AT behavior. [LEARN-HTML] [MDN-A11Y]
- MUST retain HTML validity as an authoring requirement while recognizing WCAG 2.2's removal of 4.1.1; these positions address different contracts. Why: validity checks support reliable behavior without falsely claiming a removed success criterion. [GOOGLE-HTMLCSS] [WCAG22]
- MUST treat empty and repeated-name Boolean values as valid HTML and remove the attribute for false, following WHATWG over Learn HTML's internally inconsistent repeated-name example. Why: the language standard settles semantics; Prettier owns spelling. [LEARN-HTML] [HTML-STANDARD]
- MUST implement WCAG 2.2.1 literally: allow disabling a limit, adjustment to at least ten times its default, or at least 20 seconds to extend it at least ten times, subject to its exceptions. Why: MDN's cognitive guide's factor-of-ten shorthand does not accurately describe the extension branch. [MDN-A11Y] [WCAG22]
