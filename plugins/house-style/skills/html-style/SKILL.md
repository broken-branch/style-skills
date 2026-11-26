---
name: html-style
description: "Write, edit, or review .html and rendered templates using house HTML style unless another guide is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: html
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# HTML style (house)

Our blend of the best HTML guides, in our own words. Every rule in the full guide names its source.

Scope: authored HTML Living Standard documents served as `text/html`, including assembled server-rendered pages and browser-rendered output; accessibility targets WCAG 2.2 Level AA (all applicable A and AA criteria). JSX, Vue templates, email HTML, XHTML, and third-party/generated source need their own parsing profiles. The rendered web experience still needs accessibility evaluation.

If the project declares older versions or its own formatter/linter settings, follow the project and say so.

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

## When to read more

- Before a change bigger than one function, read [references/guide.md](references/guide.md), the section for what you're doing.
- For naming basics, errors, tests, commits, secrets, and agent workflow, read [references/shared.md](references/shared.md).
- To set up tooling, copy or merge the files in [references/config/](references/config/) into your repository, then read the guide's Tooling section. Use the project's own source files and test fixtures.
- For worked controls, read [button states](references/examples/buttons.html), [field and switch](references/examples/field-switch.html), [modal focus](references/examples/dialog.html), [shared styles](references/examples/controls.css).

## Sources

See [references/sources.md](references/sources.md) for sources, licenses, source tags, and changes. Unofficial: not affiliated with or endorsed by any source's owner.
