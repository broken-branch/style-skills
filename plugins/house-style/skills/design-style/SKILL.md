---
name: design-style
description: "Build or review UI with house design tokens, typography, layout, component states, and keyboard behavior unless another look is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: design
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# Design style (house)

Build or review UI with the house visual rules. Respect a project's explicit design system and the user's requested scope.

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

- Button treatment: flat primary action, neutral secondary, rounded rectangle, no gloss. Current default, may change; no final button preference is implied. [source: house adaptation G01]
- Ownership colors: four stable paired slots, with visible owner labels and no arbitrary runtime colors. Current default, may change. [source: house adaptation G06]
- Dark theme: complete warm-neutral mapping with dark navigation. Current default, may change; visual review in an application remains open. [source: house adaptation G05]

## When to read more

- For type, density, layout, color pairs and motion, read [references/guide.md](references/guide.md).
- Before implementing controls, read the relevant state and keyboard contract in [references/components.md](references/components.md).
- Import [references/tokens.css](references/tokens.css) globally; use [references/tokens.json](references/tokens.json) for pair registries and media-query thresholds. These are filtered sync outputs; see [references/sources.md](references/sources.md) before changing them.
- For worked controls, read [control states](references/examples/controls.html), [responsive content](references/examples/layout.html), [feedback and empty states](references/examples/feedback.html), [navigation and sortable table](references/examples/navigation-table.html).

## Sources

Source tags retain the house guide's provenance. [references/sources.md](references/sources.md) explains evidence limits, transformations and licenses. Unofficial; no source owner endorses this skill.
