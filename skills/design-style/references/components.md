# Component contracts

Use the semantic tokens from [tokens.css](tokens.css), the pair registry in [tokens.json](tokens.json), and the layout rules in [guide.md](guide.md). The following contracts restate the house component guide; keyboard details complete its G10 behavior rather than claim a company's production implementation.

## Shared states

- MUST begin with native buttons, real links, labeled form controls and tables; choose action versus navigation semantics before appearance. ARIA state attributes describe behavior that the implementation must supply. [source: Shopify; house adaptation G10]
- MUST supply each applicable state below. Informational badges have no hover, focus, pressed or disabled interaction; explain such exclusions rather than adding fake controls. [source: Shopify; mockup-37; house adaptation G10]

| State | Implementation contract |
| --- | --- |
| Default | Keep readable ink, an identifiable control boundary and a stable accessible name. |
| Hover | Use the appropriate hover fill; preserve state and information for users without a pointer. |
| Focus-visible | Add the shared outline without replacing selected/invalid cues. Frame controls use frame focus ink. |
| Active / selected | Use pressed fill for transient activation; persistent selection also has a text/check marker and correct native/ARIA state. |
| Disabled | Use disabled fill and muted ink at full opacity; native disabled for unavailable controls, or a complete activation guard for `aria-disabled`. Explain the reason nearby. |
| Error | Associate a specific message with the invalid input; retain data and the focus outline. Errors are not represented solely by a red edge. |
| Loading | Retain structure, focus, action name and footprint; expose busy state and readable progress. Prevent duplicate operations. |

- MUST apply `--focus-width` / `--focus-offset` / `--color-focus` to `:focus-visible` on every control, link, summary and explicit tab stop; navigation uses `--color-focus-frame`. Leave clearance at clipping/sticky edges. [source: mockup-37; house adaptation G08]
- MUST let forced-colors mode use system foregrounds, borders and `Highlight` outlines; avoid `forced-color-adjust: none`. Add a noncolor marker for selected/invalid state. [source: Shopify; mockup-37; house adaptation G08]
- MUST keep loading actions focusable when an operation starts: use `aria-busy` plus `aria-disabled` with click/keyboard guards, and adjacent progress text. A spinner cannot be the only feedback; reduced motion uses static progress. [source: Shopify; mockup-37; house adaptation G10]

## Buttons and fields

- MUST keep one primary action per task region, with `--color-primary`, its hover/active variants, `--color-on-primary`, `--shadow-none` and `--radius-control`. Use danger tokens for destructive actions, with review/confirmation or undo appropriate to the consequence. [source: Shopify; mockup-37; house adaptation G01; house adaptation G10]
- MUST use surface/hover/active fills with text ink and control borders for secondary actions. Tertiary actions use underlined link ink on an audited neutral parent. [source: mockup-37; house adaptation G01]
- MUST use `--space-2` block / `--space-4` inline padding, `--space-2` label/icon gap and medium label weight. Both target dimensions use `--size-control`, or `--size-control-compact` in dense rows/toolbars. [source: mockup-37; house adaptation G03; house adaptation G08]
- MUST retain the matched ownership pair on hover/press, adding underline and a stronger inset edge respectively. Disabled ownership actions adopt the common disabled pair. [source: mockup-37; mockup btn-h; house adaptation G06]
- MUST give fields visible associated labels, field fill, text ink, input type size, control border/radius, and `--space-2` / `--space-3` padding. Placeholder ink stays opaque and is only an example, not a label. [source: Shopify; mockup-37; house adaptation G02; house adaptation G10]
- MUST connect help/errors with `aria-describedby`, set `aria-invalid` after meaningful validation such as blur/submit, and preserve pasted/typed values. Keep paste, autocomplete, password managers and native input affordances available. [source: Shopify; house adaptation G10]
- MUST retain the field pair on hover/focus/read-only; read-only values remain selectable. Invalid boundaries use error ink while focus remains visible; disabled fields use the common disabled pair at full opacity. [source: Shopify; house adaptation G08; house adaptation G10]
- MUST prefer native select/checkbox/radio controls and group related options with fieldset/legend. A custom replacement must reproduce naming, focus, selection and keyboard behavior before it is considered complete. [source: Shopify; house adaptation G10]

## Dialog and side detail

- MUST give a desktop nonmodal detail panel a labeled `aside`, raised fill, detail heading and close action. Move focus deliberately into it; allow navigation back to the board; closing returns focus to the opener. Do not trap focus or claim modality. [source: Notion; mockup-37; house adaptation G10]
- MUST use `dialog.showModal()` or an equivalent fully modal implementation for compact modal detail: accessible title, visible close control, inert outside content, and a visually transparent backdrop over the undimmed document. The dialog surface itself stays opaque. [source: Notion; mockup-37; house adaptation G10]
- MUST choose meaningful initial focus (a title with `tabindex="-1"` for long content, otherwise an appropriate control); Tab from the last available control wraps to the first and Shift+Tab from the first wraps to the last. If none exists, focus the dialog container. Escape closes; restore focus to the opener or a logical surviving control. Verify native dialog behavior as well as custom equivalents. [source: house adaptation G10]
- MUST preserve the selected record and visible focus when switching between side panel, modal and full-width routed detail; never hide a currently focused subtree without moving focus. [source: mockup tall-c; mockup square-c; house adaptation G04; house adaptation G10]

## Menu, tabs and combobox keys

- MUST reserve menu roles for action menus; ordinary site navigation remains links inside a navigation landmark with `aria-current`. Triggers expose `aria-expanded` and `aria-controls`; a popup action trigger also exposes `aria-haspopup="menu"`. [source: Shopify; house adaptation G10]
- MUST open an action menu with Enter/Space or ArrowDown at its first item, or ArrowUp at its last item. Within the menu, Up/Down wrap among available items, Home/End reach endpoints, and printable characters perform typeahead. Enter/Space activates. Escape dismisses and restores trigger focus; Tab closes and follows document focus order. Use roving tabindex; this menu does not trap focus. [source: house adaptation G10]
- MUST implement tabs with `tablist`, `tab`, associated `tabpanel`, `aria-selected` and roving tabindex. Left/Right wrap horizontal tabs; Up/Down serve vertical tabs; Home/End reach endpoints. Use manual selection with Enter/Space when panel work could delay activation; Tab leaves the tab list for panel content/next control. Automatic activation is suitable only for immediately available panels. [source: house adaptation G10]
- MUST use a native select unless editable filtering is necessary. An editable combobox needs a labeled input with `role="combobox"`, `aria-expanded`, `aria-controls` pointing to its listbox, and `aria-autocomplete="list"`. Options expose `aria-selected`; the input retains DOM focus and uses `aria-activedescendant` only while a matching option exists. [source: Shopify; house adaptation G10]
- MUST let typing filter an editable combobox, Down/Up open or move its active option, Enter commit it, Escape dismiss without silently replacing the typed value, and Tab dismiss and advance naturally. Keep Home/End, Left/Right and editing shortcuts native to the text input. Announce result counts/no results; clear stale active IDs when filtering or closing. [source: house adaptation G10]

## Cards, tables and feedback

- MUST build each group as a heading and card list. Give each card a title link or detail button instead of a clickable wrapper containing nested actions; selected cards have a visible marker and a clear relationship to detail. Use native selection controls for independent bulk selection. [source: Notion; mockup-32; mockup-37; house adaptation G10]
- MUST allow full titles to wrap; if a preview is clamped, provide a way to read all of it without hover. An optional drag interaction also needs a reachable move action and reorder controls where ordering matters; failures preserve the previous position and input. [source: Notion; mockup-32; house adaptation G08; house adaptation G10]
- MUST use real table headers and an accessible table name; sort via header buttons with `aria-sort` only on the current sort column. Selection uses labeled checkboxes and a mixed select-all state. Announce changes in result counts without surprising focus moves. [source: Shopify; house adaptation G10]
- MUST keep table structure during loading, distinguish a failed request from zero rows, and localize necessary horizontal scrolling to a named keyboard-accessible region with unclipped focus. [source: Shopify; house adaptation G04; house adaptation G10]
- MUST retain the current query/data through loading and failed updates. Differentiate first use, no matches, lack of permission and failures, each with a relevant next action when one exists. Use polite status announcements for routine progress/success. [source: Shopify; mockup-37; house adaptation G10; house adaptation G11]
- MUST focus a linked error summary after a failed form submission while retaining field-specific messages. Use urgent announcements sparingly and avoid duplicate announcements; essential recovery instructions cannot depend on a short-lived toast. [source: Shopify; mockup-37; house adaptation G10; house adaptation G11]
