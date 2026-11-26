# Guidelines for writing CSS code examples rules (condensed)

MDN CSS example guidance, including Prettier’s formatting baseline. Teaching-specific reset, methodology, preprocessor, browser-support and documentation-macro policies are omitted.

Each rule names its original section; examples are omitted. Source recommendations and optional choices retain their original strength.

## Quick rules

- Plan reusable base styles, layouts, and necessary overrides before growing the stylesheet. — [General guidelines for CSS code examples](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#general_guidelines_for_css_code_examples).
- Reconsider the stylesheet's organization when later rules repeatedly undo earlier declarations. — [General guidelines for CSS code examples](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#general_guidelines_for_css_code_examples).

## Tooling

- Format CSS with Prettier’s defaults; apply the guide’s additional rules afterward. — [MDN — Choosing a format](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#choosing_a_format).

No additional language-specific rules.

## Naming

- Style through classes by default, assigning IDs for purposes outside CSS. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- Default to lowercase for selectors, function names, and keyword identifiers. — [Casing](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#casing).
- Spell custom identifiers as lowercase words joined by hyphens. — [Casing](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#casing).
- Retain the established camelCase spelling of keyword values inherited from SVG. — [Casing](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#casing).

## Files and layout

- Normally put the more specific rule later when multiple rules affect the same elements. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- Start a declaration block with its custom properties, then keep properties with related purposes together. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- Separate rule blocks with empty lines unless adjacent blocks are closely related variants. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- Use an empty line within a block only when it divides distinct, meaningful groups of properties. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- Put narrow-screen defaults first, then add changes for increasingly wide viewports through media queries. — [Media queries](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#media_queries).
- Give `@import` its path as a quoted string instead of a `url()` function. — [Strings](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#strings).

## Types and data

- Use a shorthand if all of its constituent properties need values other than their defaults. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- When only some components differ from their defaults, either shorthand or individual longhands are acceptable. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- Choose the most compact equivalent shorthand and arrange its components in their canonical order. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- Use familiar color names when the design does not require a precise palette. — [Colors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#colors).
- Default to `rgb()` for a precise color, allowing hex when more convenient and other color spaces when their representation matters. — [Colors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#colors).
- Separate color-function components with spaces using modern syntax instead of commas. — [Colors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#colors).
- Choose the color function's base name without an `a` suffix, even when supplying alpha. — [Colors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#colors).
- Write hex colors with six digits, or eight when alpha is included; avoid abbreviated forms. — [Colors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#colors).
- Default color components and alpha to numbers, selecting percentages or other units only when they express the intended meaning. — [Colors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#colors).
- Leave out the alpha component when the color is fully opaque. — [Colors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#colors).
- End a font-family stack with a generic fallback; the source exempts web-safe fonts. — [Fonts](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#fonts).
- Prefer keyword weights, using `normal` for 400 and `bold` for 700; numeric weights remain appropriate for other precise values, variable-font ranges, or consistency. — [Fonts](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#fonts).
- Choose relative lengths by default, using units that track the intended font, container, or viewport relationship. — [Lengths](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#lengths).
- Use double-quoted strings wherever CSS permits leaving quotes out. — [Strings](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#strings).

## Comments and docs

- Label pseudo-CSS as plain text so readers and static checks do not mistake it for valid CSS. — [General guidelines for CSS code examples](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#general_guidelines_for_css_code_examples).
- Demonstrate functions within a property declaration, except in the dedicated first Syntax block where the reference format requires a standalone function. — [General guidelines for CSS code examples](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#general_guidelines_for_css_code_examples).
- Explain CSS that readers cannot readily understand from the code itself. — [Comments](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#comments).
- Place each explanation on its own line before the CSS it describes. — [Comments](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#comments).
- Separate comment text from both delimiting asterisks with spaces. — [Comments](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#comments).

## Testing

- Keep CSS examples parseable and remove duplicated, empty, unmatched, or otherwise ineffective code. — [General guidelines for CSS code examples](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#general_guidelines_for_css_code_examples).
- Check that colors used to distinguish elements remain distinguishable for people with color-vision deficiencies. — [Colors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#colors).
- Target a text-to-background contrast ratio of 4.5:1 or greater. — [Colors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#colors).
- Check that each fractional viewport dimension selects exactly one of the alternative media-query styles. — [Media queries](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#media_queries).

## Language-specific pitfalls

- Exclude nonstandard, deprecated, and obsolete features from ordinary code. — [General guidelines for CSS code examples](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#general_guidelines_for_css_code_examples).
- Use a prefixed feature only when its standard counterpart is unavailable. — [General guidelines for CSS code examples](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#general_guidelines_for_css_code_examples).
- For a two-endpoint animation, name the keyframes `from` and `to`. — [Animations](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#animations).
- When an animation includes intermediate frames, use percentages for every keyframe selector, including the endpoints. — [Animations](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#animations).
- Control specificity through deliberate cascade order and property organization; avoid surprising selector repetition or excessive `:where()` use. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- Use `!important` only when an essential override has no other workable solution. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- Choose either a shorthand or its component longhands; do not combine the two forms. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- An ID required for another purpose may also serve as a CSS selector, including to manage specificity. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- Introduce pseudo-elements with two colons, avoiding their historical single-colon spelling. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- Shorten compatible selector lists with `:is()`, `:where()`, or `:not()`. — [Cascade, properties, and selectors](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#cascade_properties_and_selectors).
- Express media thresholds with range comparisons rather than `min-` or `max-` syntax, including media queries in HTML attributes and JavaScript. — [Media queries](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS#media_queries).

## Where the sources disagree

This package follows one source. Its choices replace house CSS defaults for the task; existing project formatter and linter settings take precedence as described in SKILL.md.

Credit: "Guidelines for writing CSS code examples" by Mozilla Contributors, licensed under CC-BY-SA 2.5 or any later version, https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS. Adaptation licensed CC-BY-SA-4.0. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Mozilla.

## Worked examples

Read [original worked examples and their source tags](examples.md) for small applications of this guide.
