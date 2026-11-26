# House UI design

Scope: framework-neutral application UI with a dark navigation frame, warm content surfaces, compact grouped content, and a right-side detail panel when space permits. Apply within the user's task; an explicit project design system takes precedence.

## Quick rules

- MUST import the token stylesheet at application scope and express visual values through its custom properties. [source: mockup-37; house adaptation G12]
- MUST give navigation the frame color, the main workspace the sheet color, and cards the surface color; keep navigation ink on navigation surfaces. [source: Shopify; mockup-37; house adaptation G06]
- MUST select complete foreground/background pairs from the JSON registry; primary and danger actions each have their own paired label ink. [source: Shopify; mockup-37; house adaptation G08]
- MUST require unrounded contrast of at least 4.5:1 for text, including placeholders, large text and disabled labels, and 3:1 for essential boundaries and focus indicators in both themes. [source: Shopify; house adaptation G08] [WCAG22]
- MUST use the body type/leading tokens, input size for editable text, and medium-weight title tokens; leave the root font size under browser/user control. [source: mockup-37; house adaptation G02]
- MUST take padding, gaps, surface radii and elevations from their named tokens; let wrapped content increase component height. [source: Shopify; mockup-37; house adaptation G03; house adaptation G07]
- MUST treat flat primary buttons, stable ownership colors and the dark mapping as current defaults that may change, as recorded below. [source: house adaptation G01; house adaptation G06; house adaptation G05]
- MUST identify ownership and status with text as well as their distinct matching color pairs; retain full text opacity. [source: mockup-37; mockup btn-h; house adaptation G06]
- MUST use control-border ink to identify fields and outlined actions; the faint border token is decorative. [source: Shopify; house adaptation G08]
- MUST give ordinary controls a 2.75rem minimum target and dense actions at least 2rem in both dimensions, using the size tokens; prose links remain inline. [source: mockup-37; house adaptation G08]
- MUST implement applicable default, hover, focus-visible, active/selected, disabled, error and loading states without removing focus or entered data. [source: Shopify; mockup-37; house adaptation G10]
- MUST draw focus with the width/offset tokens and surface-specific focus ink; preserve system outlines in forced colors and leave room around scroll edges. [source: mockup-37; house adaptation G08]
- MUST start with native controls, visible labels and accessible names; use the component contracts for dialog, menu, tabs and combobox keyboard behavior. [source: Shopify; house adaptation G10]
- MUST collapse grouped content to one column when necessary, keep navigation/detail actions reachable, and provide a move command for any drag interaction. [source: Notion; mockup-32; mockup tall-c; mockup square-c; house adaptation G04; house adaptation G08]
- MUST distinguish a nonmodal side panel from a modal dialog; only the modal contains focus and makes the background inert. [source: Notion; mockup-37; house adaptation G10]
- MUST select themes on the root with `data-theme="light"` or `data-theme="dark"`, or omit the attribute for system preference. [source: Shopify; mockup-37; house adaptation G05]
- MUST use short tokenized feedback transitions and make nonessential motion immediate when reduced motion is requested. [source: mockup-37; house adaptation G07]
- MUST name action outcomes in sentence case and distinguish loading, empty, filtered, access-limited and failed views with useful recovery text. [source: mockup-37; house adaptation G10; house adaptation G11]

## Current defaults, may change

These are implementation choices, not settled personal preferences.

| Choice | Current default, may change | Source |
| --- | --- | --- |
| Button treatment | Flat primary fill, neutral secondary, underlined tertiary, rounded rectangular controls, no gloss or gradient. | [source: mockup button rounds; house adaptation G01] |
| Ownership colors | Four stable blue/purple/green/brown slots, always paired with readable ink and a visible owner label. No arbitrary runtime colors. | [source: mockup-37; mockup btn-h; house adaptation G06] |
| Dark content theme | Complete warm-neutral dark mapping with a dark frame in both themes; application-level visual review remains open. | [source: house adaptation G05] |

## Type and density

- MUST use the generic `--font-body` stack for UI and `--font-mono` for code/identifiers only. The public font stacks intentionally omit named font dependencies. [source: mockup-37; house adaptation G02]
- MUST use caption `.8125rem`, body `.875rem`, editable input `1rem`, section `1.125rem`, detail title `1.8125rem`, and page title `2rem` through their corresponding tokens. Body leading is `1.5`; heading leading is `1.25`. [source: Shopify; mockup-37; house adaptation G02]
- MUST use regular `400` for prose, medium `500` for labels/headings, and strong `600` for selective emphasis. Tight letter spacing belongs only on page/detail titles. [source: Shopify; mockup-37; house adaptation G02]
- MUST preserve the compact rhythm with the spacing scale: `0`, `.25`, `.5`, `.75`, `1`, `1.5`, `2`, `3rem`; card block padding is `.625rem`, board gap `.875rem`. Use the named tokens rather than repeating literals. [source: mockup-37; house adaptation G03]
- MUST inset the frame with `--space-2`, pad the sheet with `--space-5` (`--space-4` in compact mode), and pad cards inline with `--space-3`. Minimum targets use `--size-control` and `--size-control-compact`, not padding alone. At a 16px root these are 44px and 32px; do not shrink them to achieve density. [source: mockup-37; house adaptation G03; house adaptation G08]

## Layout

- MUST treat sidebar `14.5rem`, detail `27rem`, board column `14.375rem`, rail `3.5rem`, and reading width `45rem` as tokenized preferred dimensions, with shrinkable tracks and no fixed page minimum size. [source: Notion; mockup-32; mockup-37; house adaptation G04]
- MUST derive responsive queries from the JSON thresholds: wide `76rem`, split `64rem`, compact `42rem`, short height `44rem`. CSS variables do not work in media-query conditions; annotate each literal with its JSON key and update it on token changes. [source: mockup tall-c; mockup square-c; house adaptation G04]
- MUST use sidebar/board/optional side detail at or above wide; below wide, use a rail with split content only when width is at least split and height is at most short. Otherwise use a top navigation strip and deliberate routed/modal detail. [source: mockup tall-c; mockup square-c; house adaptation G04]
- MUST stack groups below split and reduce sheet padding below compact. Complementary width comparisons must leave no fractional gaps. When enlarged text needs more space, reflow earlier. [source: Notion; mockup-32; house adaptation G04]
- MUST keep desktop board overflow inside a named region and retain a single-column path; only genuinely two-dimensional tables may keep their own horizontal scroller on small screens. Preserve every action and the reading order. [source: Notion; mockup-32; house adaptation G04; house adaptation G08]

## Color and contrast

- MUST use opaque registered surfaces behind text. Avoid faded text, mixed status pairs, text over gradients/images, and using shadow as a control boundary. Color names describe roles, not permission to combine any two tokens. [source: mockup-37; house adaptation G08]
- MUST keep links underlined, use the matching status ink for all banner content (including links), and place boxed retry actions on a neutral surface outside the banner. Ordinary muted/link colors are not registered on tinted banners. [source: Shopify; house adaptation G06; house adaptation G10]
- MUST use `--color-owner-{blue,purple,green,brown}-{surface,text}` as stable paired ownership slots, with a visible label. Ownership is separate from success/caution/warning/error state. [source: mockup-37; mockup btn-h; house adaptation G06]
- MUST check new text or indicator combinations in each theme before adding them to `textPairs` or `nonTextPairs`. Compare full-precision ratios, never rounded display values. The relative luminance calculation uses opaque sRGB linearized at `0.04045`, weighted by `0.2126`, `0.7152`, `0.0722`; contrast is `(lighter + .05) / (darker + .05)`. [source: Shopify; mockup-37; house adaptation G12] [WCAG22]
- MUST retain the entire semantic mapping and native `color-scheme` together when changing theme. System mode has no root theme attribute; an explicit root override also reaches portaled content. [source: Shopify; mockup-37; house adaptation G05]

## Geometry, motion and icons

- MUST use tag/nav/control/card/popover/sheet radii by role. Reserve pill radii for compact status badges; join sheet and side-panel edges flush. Use the compact sheet radius where appropriate. [source: Shopify; mockup-37; mockup tall-c; mockup square-c; house adaptation G01; house adaptation G04]
- MUST assign card, popover and dialog shadows and base/sticky/popover/dialog layer tokens to their corresponding surfaces; preserve focus visibility across stacking contexts. [source: mockup-37; house adaptation G07; house adaptation G08]
- MUST transition color, boundary color and shadow with `--duration-fast` and `--ease-standard`; optional panel transforms use `--duration-panel`. Reduced motion also stops any nonessential animation outside the token stylesheet. [source: mockup-37; house adaptation G07]
- MUST use original outline icons with `--size-icon`, `--icon-stroke` and inherited ink. Hide redundant icons from assistive technology and give icon-only actions a persistent name plus discoverable text help. No icon library is required. [source: Shopify; mockup-37; house adaptation G09]

## Adoption and verification

Read [components.md](components.md) before implementing the relevant control. The [examples](examples/controls.html) are local HTML/CSS studies, not a complete application component library.

- MUST import [tokens.css](tokens.css) globally, outside scoped component styles; use classes in any framework. [tokens.json](tokens.json) defines the pair and breakpoint contract. [source: mockup-37; house adaptation G12]
- MUST update source tokens through the maintainer sync workflow in [sources.md](sources.md); keep downstream overrides explicit and audit their new combinations. A token change does not silently settle any provisional visual choice. [source: house adaptation G12]
- MUST verify both themes, all applicable states, long labels, text zoom/spacing, narrow reflow, keyboard order, visible focus, dialog entry/wrap/return, accessible names, forced colors and reduced motion in the consuming application. Static pair checks alone establish neither rendered accessibility nor complete conformance. [source: Shopify; mockup-37; house adaptation G08]
