# CSS style guide

Scope: hand-authored standard CSS for browser applications and component libraries, including native nesting and cascade layers where the application's supported browsers allow them. The tooling baseline is Stylelint 17.16.0 with standard 40.0.0 and recommended 18.0.0; generated/vendor CSS, Sass, CSS-in-JS, and framework-specific syntax need separate profiles.
Baseline: [shared rules](shared.md), including dependencies, commits, versioning, review, and AI agent workflow.
MUST means required; PREFER means the default, with a reason recorded for departures.
Source tags resolve in [source credits](sources.md#source-tags).

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

## Tooling

| Purpose | Tool and version | Config file | Repository command |
| --- | --- | --- | --- |
| Formatter | Prettier 3.9.10 | [Root web `.prettierrc.json`](config/.prettierrc.json) | `npx prettier --check .` |
| Linter | Stylelint 17.16.0; stylelint-config-standard 40.0.0; stylelint-config-recommended 18.0.0; Node 24 LTS or a newer supported release | [`.stylelintrc.json`](config/.stylelintrc.json) | `npx stylelint "src/**/*.css" --max-warnings 0` |
| Build / type checks | No standalone CSS type checker or compiler | Consuming application's browser support and build configuration | No standalone build command; use the application's existing build. |
| Tests | Consuming application's pinned browser/visual runner; none bundled | Browser cases in Testing below | No standalone browser test command; use the application's existing suite. |

Mechanical formatting: the formatter handles this. Copy [the single web config](config/.prettierrc.json) to the consuming repository root as `.prettierrc.json`; do not add competing language configs. TypeScript/TSX and Vue scripts use `singleQuote: true`; standalone `*.css` uses `false`. Vue `<style>` uses the SFC's `true` setting too. Only `*.html` disables embedded-language formatting; Vue scripts/styles remain formatted. [PRETTIER]

Run these commands from the project root after copying the Stylelint config and shared Prettier config, installing the listed package versions, and selecting the project’s authored CSS files.

Prettier's `singleQuote`, `tabWidth`, `useTabs`, `printWidth`, and `endOfLine` options own mechanical presentation; `printWidth` is a wrapping preference. Stylelint's `--fix` applies available lint fixes, followed by Prettier and then both checks. Quote presence in URLs, attributes, and font families remains a lint check; the formatter owns quote character selection. [PRETTIER] [STYLELINT]

Prettier 3.9.10 and Stylelint 17.16.0 passed on a sample stylesheet. Validate the adopted configuration and browser behavior in the consuming application.

- MUST apply this Stylelint profile to authored plain `.css` files; configure an appropriate parser and rules separately for SCSS, Vue styles, CSS Modules extensions, or CSS-in-JS. Why: plain-CSS rules cannot validate every embedded dialect. [STYLELINT]

Vue SFC styles follow these semantic rules by review; the [Vue profile](related/vue.md#tooling) explicitly ships no Stylelint SFC parser. A project adding automated coverage uses `postcss-html` for `.vue` and validates its Vue-specific selectors rather than applying the plain-CSS parser blindly.

### Enabled Stylelint rules

Every enabled rule ID is listed below. The inherited inventory comes from standard 40.0.0 and recommended 18.0.0, with the explicit overrides shown afterward; all enabled rules use error severity. These are detection summaries, not a claim that static lint proves rendering or accessibility. [STYLELINT-STANDARD] [STYLELINT]

| Inherited rule ID | Detection / selected policy |
| --- | --- |
| `alpha-value-notation` | Percentage color alpha; numeric opacity/fill-opacity/flood-opacity/stop-opacity/stroke-opacity. |
| `annotation-no-unknown` | Unknown annotations. |
| `at-rule-descriptor-no-unknown` | Unknown descriptors. |
| `at-rule-descriptor-value-no-unknown` | Invalid descriptor values. |
| `at-rule-no-deprecated` | Deprecated at-rules. |
| `at-rule-no-unknown` | Unknown at-rules. |
| `at-rule-no-vendor-prefix` | Vendor-prefixed at-rule names. |
| `at-rule-prelude-no-invalid` | Invalid preludes, except media handled separately. |
| `block-no-empty` | Empty blocks. |
| `block-no-redundant-nested-style-rules` | Unnecessary nested style wrappers. |
| `color-function-alias-notation` | Alpha-free function names. |
| `color-function-notation` | Modern color syntax. |
| `color-hex-length` | Shortest equivalent hex. |
| `comment-no-empty` | Empty comments. |
| `container-name-pattern` | Kebab-case, optionally prefixed with --. |
| `custom-media-pattern` | Kebab-case custom media names. |
| `custom-property-no-missing-var-function` | Bare custom-property references missing var(). |
| `custom-property-pattern` | Kebab-case custom property names after --. |
| `declaration-block-no-duplicate-custom-properties` | Duplicate token declarations in a block. |
| `declaration-block-no-duplicate-properties` | Duplicate properties; consecutive different-syntax fallbacks allowed. |
| `declaration-block-no-redundant-longhand-properties` | Complete redundant longhand sets. |
| `declaration-block-no-shorthand-property-overrides` | Shorthand overwriting earlier constituent declarations. |
| `declaration-property-value-keyword-no-deprecated` | Deprecated value keywords. |
| `declaration-property-value-no-unknown` | Unknown property/value combinations. |
| `font-family-name-quotes` | Quotes only where recommended; simple Arial stays unquoted. |
| `font-family-no-duplicate-names` | Duplicate font families. |
| `font-family-no-missing-generic-family-keyword` | Missing generic fallback; system-font/inheritance/variable exceptions. |
| `function-calc-no-unspaced-operator` | Invalid calculation operator spacing. |
| `function-name-case` | Lowercase CSS function names. |
| `function-url-quotes` | Quoted url() arguments. |
| `hue-degree-notation` | Angle-unit hue. |
| `import-notation` | url() import form. |
| `keyframe-block-no-duplicate-selectors` | Repeated keyframe selectors. |
| `keyframe-declaration-no-important` | Ineffective important keyframe declarations. |
| `keyframe-selector-notation` | Percentages, except keyword-only from/to blocks. |
| `keyframes-name-pattern` | Kebab-case animation names. |
| `layer-name-pattern` | Kebab-case segments with optional dot-separated hierarchy. |
| `length-zero-no-unit` | Unitless zero lengths, except custom properties. |
| `lightness-notation` | Percentage lightness in lab/lch/oklab/oklch. |
| `media-feature-name-no-unknown` | Unknown media features. |
| `media-feature-name-no-vendor-prefix` | Vendor-prefixed media features. |
| `media-feature-name-value-no-unknown` | Unknown media feature/value combinations. |
| `media-feature-range-notation` | Context/range comparison syntax. |
| `media-query-no-invalid` | Invalid media queries. |
| `media-type-no-deprecated` | Deprecated media types. |
| `named-grid-areas-no-invalid` | Invalid named-grid area definitions. |
| `nesting-selector-no-missing-scoping-root` | Nesting selector without a scoping root. |
| `no-descending-specificity` | Potentially confusing lower-specificity rules after higher ones. |
| `no-duplicate-at-import-rules` | Duplicate imports. |
| `no-duplicate-selectors` | Duplicate selectors in a shared context. |
| `no-empty-source` | Empty stylesheets. |
| `no-invalid-double-slash-comments` | Invalid // comments. |
| `no-invalid-position-at-import-rule` | Imports in invalid positions. |
| `no-invalid-position-declaration` | Declarations in invalid positions. |
| `no-irregular-whitespace` | Unexpected whitespace characters. |
| `number-max-precision` | At most four decimal places. |
| `property-no-deprecated` | Deprecated properties. |
| `property-no-unknown` | Unknown properties. |
| `property-no-vendor-prefix` | Vendor-prefixed property names. |
| `selector-anb-no-unmatchable` | An+B expressions that cannot match. |
| `selector-attribute-quotes` | Quoted attribute-selector values. |
| `selector-class-pattern` | Kebab-case classes; BEM underscores rejected. |
| `selector-no-vendor-prefix` | Vendor-prefixed selectors. |
| `selector-not-notation` | Complex negation list notation. |
| `selector-pseudo-class-no-unknown` | Unknown pseudo-classes. |
| `selector-pseudo-element-colon-notation` | Double-colon pseudo-elements. |
| `selector-pseudo-element-no-unknown` | Unknown pseudo-elements. |
| `selector-type-case` | Lowercase type selectors. |
| `selector-type-no-unknown` | Unknown type selectors; custom elements allowed. |
| `shorthand-property-no-redundant-values` | Redundant repeated shorthand values. |
| `string-no-newline` | Invalid string newlines; at-rule preludes and declaration values ignored. |
| `syntax-string-no-invalid` | Invalid syntax descriptor strings. |
| `value-keyword-case` | Lowercase keywords, including currentcolor. |
| `value-no-vendor-prefix` | Vendor-prefixed values, except box/inline-box forms. |

House additions use the same Stylelint 17.16.0 core; no plugins are required. [STYLELINT]

| Added rule ID | Detection / selected policy |
| --- | --- |
| `declaration-no-important` | true: rejects important declarations unless a narrowly explained accessibility exception disables this rule. |
| `function-url-no-scheme-relative` | true: rejects protocol-relative url() arguments. |
| `function-url-scheme-allowed-list` | https/data/blob: restricts explicit url() schemes; relative URLs remain valid. |
| `max-nesting-depth` | 2: counts nested rules/at-rules, excluding root-level at-rule wrappers. |
| `selector-max-id` | 0: rejects ID selectors. |
| `selector-no-qualifying-type` | true, ignore attribute: rejects tag-qualified classes; permits input[type]. |

### Overrides and coverage limits

| Disabled rule ID | Reason |
| --- | --- |
| `at-rule-empty-line-before` | Mechanical layout is delegated to Prettier. |
| `comment-empty-line-before` | Mechanical layout is delegated to Prettier. |
| `comment-whitespace-inside` | No separate hand-authored comment-spacing policy. |
| `custom-property-empty-line-before` | Mechanical layout is delegated to Prettier. |
| `declaration-block-single-line-max-declarations` | Block layout is delegated to Prettier; the stable preset's value differs from development main. |
| `declaration-empty-line-before` | Related-property grouping remains a review choice. |
| `rule-empty-line-before` | Mechanical layout is delegated to Prettier. |
| `selector-id-pattern` | ID selectors are prohibited by `selector-max-id: 0`, making their spelling irrelevant. |

The configuration also enables `reportDescriptionlessDisables`, `reportInvalidScopeDisables`, `reportNeedlessDisables`, and `reportUnscopedDisables`. These are configuration option IDs, not CSS rule IDs: they detect missing explanations, nonexistent configured rule scopes, redundant suppressions, and disables that name no rules. Shared policy governs whether an exception is justified. [STYLELINT]

For an unavoidable state-enforcing utility (`hidden` or visually-hidden) or global reduced-motion reset, keep `declaration-no-important` enabled and explain the exact declaration:

```css
[hidden]:not([hidden="until-found"]) {
  /* stylelint-disable-next-line declaration-no-important -- keep hidden state authoritative over component display rules */
  display: none !important;
}
```

Keep `hidden="until-found"` behavior intact. Prefer a local motion override without `!important` when it works. Important declarations reverse cascade-layer order: earlier layers outrank later layers, and layered important declarations outrank unlayered important declarations. Review the layer placement of exceptions. [MDN important](https://developer.mozilla.org/en-US/docs/Web/CSS/important) [STYLELINT]

Manual review covers component boundaries, token meaning, declaration grouping, deliberate shorthand resets, ARIA/data state semantics, browser support, runtime custom-property values, and trust in asset URLs. Browser tests cover actual layout, accessibility, focus, color contrast, and motion. `no-descending-specificity` has no DOM knowledge and cannot prove two selectors overlap. The URL checks inspect literal `url()` schemes, ignore variable arguments and URLs without schemes, and do not sanitize CSS or check remote destinations. [STYLELINT] [WEBDEV-CSS]

## Naming

- MUST use lowercase kebab-case for CSS classes, custom properties, animation names, and container names; layer segments use kebab-case separated by dots. Why: the standard preset checks these authored identifiers consistently. [STYLELINT-STANDARD]
- MUST use class selectors instead of ID selectors for component styling, even when an element needs an ID for anchors or accessibility. Why: class-based styles remain reusable without ID specificity. [GOOGLE-CSS]
- MUST omit element qualifiers from class selectors, such as `button.card-toggle`; type-qualified attributes such as `input[type="checkbox"]` are allowed. Why: component classes should not depend on a specific HTML tag. [GOOGLE-CSS] [STYLELINT]
- PREFER existing native state selectors or genuine ARIA state attributes for accessible widget state, and `data-*` attributes for purely visual variants. Why: styling the authoritative state avoids a second drifting class flag. [MDN-ARIA-STATE] [CUBE-CSS]
- PREFER component prefixes for public selectors and custom properties in embeddable widgets. Why: independently loaded styles can otherwise collide in the host page. [GOOGLE-CSS]

## Files and layout

- PREFER plain CSS with CUBE-style composition, small single-purpose utilities, component blocks, and explicit state exceptions. Why: layout relationships can be reused without coupling them to decoration. [CUBE-CSS]
- PREFER shared inherited defaults and an explicit cascade-layer order before component rules. Why: planned priority avoids repeated overrides and escalating specificity. [CUBE-CSS] [WEBDEV-CSS]
- MUST resolve ordinary overrides through cascade structure; allow `!important` only for evidenced global reduced-motion resets or state-enforcing utilities with a rule-specific, explained disable. Why: narrow accessibility exceptions preserve intent without routine priority escalation. [GOOGLE-CSS] [MDN-CSS] [STYLELINT]
- MUST limit nesting to two levels inside a style rule, counting nested at-rules as levels; root-level at-rule wrappers do not count. Why: shallow nesting limits hidden selector relationships. [WEBDEV-CSS] [STYLELINT]
- PREFER related-property groups with custom properties first, preserving the order of fallback declarations. Why: semantic groups explain a block without accidentally changing the cascade. [MDN-CSS] [WEBDEV-CSS]
- PREFER flexbox for one-dimensional arrangement and grid for two-dimensional layout, allowing content to wrap and grow. Why: intrinsic layout tolerates different content and available space. [WEBDEV-CSS] [CUBE-CSS]
- PREFER narrow-screen base styles with wider changes expressed by range media queries. Why: the usable baseline needs fewer overrides on small screens. [MDN-CSS]

## Types and data

- PREFER semantic custom properties for shared colors, spacing, and typography, with global defaults on `:root` and component overrides kept local. Why: tokens support consistent theming through the cascade. [CUBE-CSS] [WEBDEV-CSS]
- MUST reference custom properties with `var()` and provide a valid fallback when an optional token can be missing. Why: unresolved substitutions can invalidate a declaration. [MDN-CSS-VARS] [STYLELINT-STANDARD]
- PREFER relative units suited to the relationship being expressed, and unitless `line-height` for inheritable text rhythm. Why: sizing should respond to fonts, containers, and user settings. [MDN-CSS] [WEBDEV-CSS]
- PREFER logical sizing, spacing, and alignment properties when layout should follow writing direction. Why: inline/block relationships adapt to right-to-left and vertical text. [WEBDEV-CSS]
- PREFER `box-sizing: border-box` for application layout, including pseudo-elements. Why: declared dimensions then include border and padding. [WEBDEV-CSS]
- PREFER longhands for partial changes and keep each property family consistently shorthand or longhand within a declaration block. Why: omitted shorthand constituents reset values that callers may rely on. [MDN-CSS] [WEBDEV-CSS]
- MUST use a generic family at the end of ordinary `font-family` and `font` family lists, including after web-safe names. Why: named fonts can still be unavailable on a user's system. [STYLELINT-STANDARD] [WEBDEV-CSS]
- MUST use modern `rgb()`/`hsl()` notation without alpha-suffixed aliases and the shortest equivalent hex form when choosing hex. Why: the selected preset provides one mechanically checked representation. [STYLELINT-STANDARD] [GOOGLE-CSS]
- MUST use percentage color alpha, angle units for hue, and percentage lightness in `lab()`/`lch()`/`oklab()`/`oklch()`; use numeric `opacity`, `fill-opacity`, `flood-opacity`, `stop-opacity`, and `stroke-opacity`. Why: the preset's explicit property exceptions differ from its color-function defaults. [STYLELINT-STANDARD]
- MUST retain valid units in custom-property tokens when their consuming expressions need dimensions, even for zero. Why: a token later substituted into a calculation must have the right type. [STYLELINT-STANDARD] [WEBDEV-CSS]

## Errors

- MUST provide a working baseline before progressively enhancing with features outside the supported browser matrix, using supported fallback declarations or `@supports` where appropriate. Why: unsupported CSS is ignored rather than reported as an application exception. [WEBDEV-CSS] [CUBE-CSS]
- MUST check substituted custom-property values against the receiving property's grammar; `var(--token, fallback)` does not rescue a defined token of the wrong type. Why: invalid-at-computed-value declarations use initial/inherited behavior rather than an earlier declaration. [MDN-CSS-VARS]
- MUST keep text legible when background images or web fonts fail to load. Why: resource failure must not erase the foreground/background relationship. [WEBDEV-CSS]

## Comments and docs

- PREFER documenting a component's configurable CSS custom properties, inheritance expectations, layer placement, and state selectors beside its styles. Why: these are the integration contract for callers and themes. [CUBE-CSS] [MDN-CSS-VARS]
- PREFER annotating browser-specific CSS workarounds with the affected feature and the condition under which the workaround can be removed. Why: a deliberate compatibility exception should not become permanent unexplained CSS. [GOOGLE-CSS] [MDN-CSS]

## Testing

- MUST preserve a visible keyboard focus indicator, including forced-colors mode; do not remove outlines without an accessible replacement. Why: keyboard users need to locate the active control. [WEBDEV-CSS]
- MUST preserve meaningful DOM and focus order rather than repair content order with flex/grid reordering. Why: visual order can diverge from keyboard and assistive-technology navigation. [WEBDEV-CSS]
- MUST respect `prefers-reduced-motion` for nonessential motion and preserve the underlying interaction when motion is removed. Why: motion must remain controllable (house choice beyond AA; WCAG 2.3.3 is AAA). [WEBDEV-CSS] [WCAG22]
- MUST verify CSS changes at narrow and wide sizes, with long content, missing fonts/images, keyboard navigation, forced colors, and reduced motion in supported browsers. Why: a stylesheet that parses can still clip content or hide controls. [WEBDEV-CSS]
- MUST meet WCAG 2.2 AA text contrast: 4.5:1 for ordinary text and 3:1 for large text, applying the criterion's exceptions. Why: palette choices must remain readable. [WCAG22]
- MUST verify required UI indicators against WCAG 1.4.11, retain noncolor state cues, and keep focus from being entirely obscured. Why: color and layering can conceal controls or their state. [WCAG22]
- MUST verify 200% text resizing, user text-spacing overrides, and reflow at 320 CSS pixels for vertical content or 256 CSS pixels high for horizontal content, with WCAG's two-dimensional-content exception. Why: layout must tolerate magnification and spacing changes. [WCAG22]
- MUST check pointer targets against WCAG 2.5.8's 24-by-24 CSS-pixel minimum or its spacing and other exceptions. Why: tightly packed controls are difficult to activate. [WCAG22]

## Performance

- PREFER animating `transform` and `opacity` when they express the intended effect. Why: repeatedly animating layout dimensions can trigger expensive layout work. [WEBDEV-CSS]

## Security

- MUST use explicit HTTPS for remote stylesheet, font, and image URLs, avoiding HTTP and protocol-relative URLs; relative paths and project-controlled `data:`/`blob:` assets are allowed. Why: embedded CSS resources must not introduce insecure transport. [GOOGLE-CSS] [OWASP] [STYLELINT]
- MUST map untrusted theme inputs to allowed CSS property/value pairs instead of interpolating arbitrary selectors, declarations, or `url()` content. Why: CSS injection can change the interface and trigger external requests. [OWASP]

## Language-specific pitfalls

- MUST account for cascade-layer priority before comparing selector specificity: normal unlayered author rules outrank normal layered author rules. Why: adding a more specific selector inside a layer may still lose. [WEBDEV-CSS]
- MUST distinguish `:where()`'s zero specificity from `:is()`/`:not()`/`:has()` and native nesting contributions. Why: a selector list can raise priority beyond the visibly matching branch. [WEBDEV-CSS]
- MUST treat `z-index` as local to its stacking context rather than a page-wide ordering number. Why: a large child value cannot escape an ancestor's context. [WEBDEV-CSS]
- MUST avoid concealing meaningful overflow merely to make a layout fit, and keep necessary scrolling keyboard-accessible. Why: clipping and scroll traps can make content unreachable. [WEBDEV-CSS]
- MUST keep adjacent media-query alternatives gap-free at fractional dimensions. Why: viewport sizes are not restricted to integer CSS pixels. [MDN-CSS]
- MUST query an eligible ancestor when using size container queries and declare its appropriate `container-type`. Why: an element cannot choose its own styles from its own queried size. [WEBDEV-CSS]
- MUST use current feature references for `:has()` and numeric font weights instead of web.dev Learn CSS's older parent-selection and 100-step-only claims. Why: relational selection exists and supported fonts can use weights across 1–1000. [WEBDEV-CSS] [MDN-CSS-CURRENT]

## Where the sources disagree

Where the sources disagree, the following house choices apply. Each choice states the adopted behavior and its reason.

- MUST use the standard preset's short hex policy, agreeing with Google over MDN's six/eight-digit-only examples. Why: one enabled check handles equivalent color representations consistently. [GOOGLE-CSS] [MDN-CSS] [STYLELINT-STANDARD]
- MUST accept the root config's double quotes in standalone `.css` and single quotes in Vue `<style>` blocks, choosing the CSS override for plain files and the SFC setting for embedded styles. Why: one formatter config makes the file-context distinction explicit; MDN and Google prefer different quote characters. [GOOGLE-CSS] [MDN-CSS] [PRETTIER]
- MUST retain `function-url-quotes: "always"`, following MDN and Stylelint over Google's unquoted URL convention. Why: quote presence is automatically checked without a second manual formatting policy. [GOOGLE-CSS] [MDN-CSS] [STYLELINT-STANDARD]
- MUST use `import-notation: "url"` for any retained imports, following Stylelint over MDN's bare-string imports. Why: a single syntax is automatically enforceable. [MDN-CSS] [STYLELINT-STANDARD]
- MUST use Stylelint's percentage color alpha and numeric opacity-property exceptions over MDN's general numeric default. Why: the released preset explicitly distinguishes these contexts. [MDN-CSS] [STYLELINT-STANDARD]
- MUST use Stylelint's angle-unit hue policy over MDN's general numeric default. Why: the preset gives all authors the same checked representation. [MDN-CSS] [STYLELINT-STANDARD]
- MUST use percentage lightness where the selected Stylelint rule applies, overriding MDN's general numeric default where both are permitted. Why: the rule's function-specific scope prevents incompatible conventions. [MDN-CSS] [STYLELINT-STANDARD]
- PREFER related-property groups with custom properties first, choosing MDN's organization within Google's project-consistency requirement instead of its optional alphabetical fallback. Why: grouping exposes intent while preserving cascade-sensitive declaration order. [GOOGLE-CSS] [MDN-CSS]
- MUST use classes for styling even when an ID is independently justified, choosing Google's class-only policy over MDN's specificity exception. Why: `selector-max-id: 0` provides a clear reusable-component boundary. [GOOGLE-CSS] [MDN-CSS] [STYLELINT]
- PREFER MDN's selective shorthand and unmixed-property-family policy over Google's shorthand-wherever-practical default. Why: a partial change should not silently reset other constituents; lint catches earlier longhands overridden by shorthand, while review covers the reverse direction. [GOOGLE-CSS] [MDN-CSS] [STYLELINT-STANDARD]
- PREFER plain CSS organized with CUBE concepts for products; keep MDN's no-methodology/no-preprocessor restrictions scoped to its teaching examples. Why: CUBE permits any CSS-producing tool, but this deliverable intentionally validates plain CSS only. [CUBE-CSS] [MDN-CSS]
- MUST keep class names within the standard preset's kebab-case pattern, using names such as `card-title` instead of CUBE's optional BEM-style `card__title`. Why: the selected naming check defines the product convention CUBE leaves to the team. [CUBE-CSS] [STYLELINT-STANDARD]
- PREFER genuine native/ARIA state hooks when an exception has accessibility meaning, following MDN there and reserving CUBE's data attributes for visual variants. Why: one authoritative state avoids duplicated accessibility and appearance flags. [CUBE-CSS] [MDN-ARIA-STATE]
- MUST omit or replace a remote CSS resource that lacks HTTPS, rejecting Google's conditional HTTP fallback in favor of OWASP's secure-transport policy. Why: a reusable stylesheet must not introduce mixed content into authenticated pages. [GOOGLE-CSS] [OWASP]
- MUST retain `font-family-name-quotes: "always-where-recommended"`, choosing Stylelint's rejection of unnecessary simple-family quotes over MDN's optional-string quoting. Why: the linter owns where font-family quotes are needed, and Prettier owns their character. [MDN-CSS] [STYLELINT-STANDARD] [PRETTIER]
- MUST retain a generic family after ordinary font names, choosing recommended 18.0.0 over MDN's web-safe-fallback exception. Why: a locally available named font is not guaranteed on every system; system-font and inherited-value rule exceptions remain valid. [MDN-CSS] [STYLELINT-STANDARD]
- MUST accept the preset's lowercase keyword policy, including `currentcolor`, over MDN's SVG-derived `currentColor` spelling. Why: `value-keyword-case` supplies one consistent result without altering case-sensitive identifiers. [MDN-CSS] [STYLELINT-STANDARD]
