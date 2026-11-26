---
name: css-style
description: "Write, edit, or review .css and component styles using house CSS style unless another guide is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: css
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# CSS style (house)

Our blend of the best CSS guides, in our own words. Every rule in the full guide names its source.

Scope: hand-authored standard CSS for browser applications and component libraries, including native nesting and cascade layers where the application's supported browsers allow them. The tooling baseline is Stylelint 17.16.0 with standard 40.0.0 and recommended 18.0.0; generated/vendor CSS, Sass, CSS-in-JS, and framework-specific syntax need separate profiles.

If the project declares older versions or its own formatter/linter settings, follow the project and say so.

## Quick rules

- MUST use lowercase kebab-case for CSS classes, custom properties, animation names, and container names; layer segments use kebab-case separated by dots. Why: the standard preset checks these authored identifiers consistently. [STYLELINT-STANDARD]
- MUST use class selectors instead of ID selectors for component styling, even when an element needs an ID for anchors or accessibility. Why: class-based styles remain reusable without ID specificity. [GOOGLE-CSS]
- MUST omit element qualifiers from class selectors, such as `button.card-toggle`; type-qualified attributes such as `input[type="checkbox"]` are allowed. Why: component classes should not depend on a specific HTML tag. [GOOGLE-CSS] [STYLELINT]
- PREFER existing native state selectors or genuine ARIA state attributes for accessible widget state, and `data-*` attributes for purely visual variants. Why: styling the authoritative state avoids a second drifting class flag. [MDN-ARIA-STATE] [CUBE-CSS]
- PREFER plain CSS with CUBE-style composition, small single-purpose utilities, component blocks, and explicit state exceptions. Why: layout relationships can be reused without coupling them to decoration. [CUBE-CSS]
- PREFER shared inherited defaults and an explicit cascade-layer order before component rules. Why: planned priority avoids repeated overrides and escalating specificity. [CUBE-CSS] [WEBDEV-CSS]
- MUST resolve ordinary overrides through cascade structure; allow `!important` only for evidenced global reduced-motion resets or state-enforcing utilities with a rule-specific, explained disable. Why: narrow accessibility exceptions preserve intent without routine priority escalation. [GOOGLE-CSS] [MDN-CSS] [STYLELINT]
- MUST limit nesting to two levels inside a style rule, counting nested at-rules as levels; root-level at-rule wrappers do not count. Why: shallow nesting limits hidden selector relationships. [WEBDEV-CSS] [STYLELINT]
- PREFER flexbox for one-dimensional arrangement and grid for two-dimensional layout, allowing content to wrap and grow. Why: intrinsic layout tolerates different content and available space. [WEBDEV-CSS] [CUBE-CSS]
- PREFER narrow-screen base styles with wider changes expressed by range media queries. Why: the usable baseline needs fewer overrides on small screens. [MDN-CSS]
- PREFER semantic custom properties for shared colors, spacing, and typography, with global defaults on `:root` and component overrides kept local. Why: tokens support consistent theming through the cascade. [CUBE-CSS] [WEBDEV-CSS]
- MUST reference custom properties with `var()` and provide a valid fallback when an optional token can be missing. Why: unresolved substitutions can invalidate a declaration. [MDN-CSS-VARS] [STYLELINT-STANDARD]
- PREFER relative units suited to the relationship being expressed, and unitless `line-height` for inheritable text rhythm. Why: sizing should respond to fonts, containers, and user settings. [MDN-CSS] [WEBDEV-CSS]
- PREFER logical sizing, spacing, and alignment properties when layout should follow writing direction. Why: inline/block relationships adapt to right-to-left and vertical text. [WEBDEV-CSS]
- PREFER longhands for partial changes and keep each property family consistently shorthand or longhand within a declaration block. Why: omitted shorthand constituents reset values that callers may rely on. [MDN-CSS] [WEBDEV-CSS]
- MUST use a generic family at the end of ordinary `font-family` and `font` family lists, including after web-safe names. Why: named fonts can still be unavailable on a user's system. [STYLELINT-STANDARD] [WEBDEV-CSS]
- MUST provide a working baseline before progressively enhancing with features outside the supported browser matrix, using supported fallback declarations or `@supports` where appropriate. Why: unsupported CSS is ignored rather than reported as an application exception. [WEBDEV-CSS] [CUBE-CSS]
- MUST check substituted custom-property values against the receiving property's grammar; `var(--token, fallback)` does not rescue a defined token of the wrong type. Why: invalid-at-computed-value declarations use initial/inherited behavior rather than an earlier declaration. [MDN-CSS-VARS]
- MUST preserve a visible keyboard focus indicator, including forced-colors mode; do not remove outlines without an accessible replacement. Why: keyboard users need to locate the active control. [WEBDEV-CSS]
- MUST preserve meaningful DOM and focus order rather than repair content order with flex/grid reordering. Why: visual order can diverge from keyboard and assistive-technology navigation. [WEBDEV-CSS]
- MUST respect `prefers-reduced-motion` for nonessential motion and preserve the underlying interaction when motion is removed. Why: motion must remain controllable (house choice beyond AA; WCAG 2.3.3 is AAA). [WEBDEV-CSS] [WCAG22]
- MUST verify CSS changes at narrow and wide sizes, with long content, missing fonts/images, keyboard navigation, forced colors, and reduced motion in supported browsers. Why: a stylesheet that parses can still clip content or hide controls. [WEBDEV-CSS]
- MUST meet WCAG 2.2 AA text contrast: 4.5:1 for ordinary text and 3:1 for large text, applying the criterion's exceptions. Why: palette choices must remain readable. [WCAG22]
- MUST use explicit HTTPS for remote stylesheet, font, and image URLs, avoiding HTTP and protocol-relative URLs; relative paths and project-controlled `data:`/`blob:` assets are allowed. Why: embedded CSS resources must not introduce insecure transport. [GOOGLE-CSS] [OWASP] [STYLELINT]

## When to read more

- Before a change bigger than one function, read [references/guide.md](references/guide.md), the section for what you're doing.
- For naming basics, errors, tests, commits, secrets, and agent workflow, read [references/shared.md](references/shared.md).
- To set up tooling, copy or merge the files in [references/config/](references/config/) into your repository, then read the guide's Tooling section. Use the project's own source files and test fixtures.
- For worked controls, read [preview](references/examples/preview.html), [button states](references/examples/buttons.css), [field and switch](references/examples/fields.css), [wrapping layout](references/examples/layout.css).

## Sources

See [references/sources.md](references/sources.md) for sources, licenses, source tags, and changes. Unofficial: not affiliated with or endorsed by any source's owner.
