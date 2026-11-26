# Airbnb React/JSX rules

Airbnb’s historical React guide, condensed. Dated rules are marked and current React compatibility notes appear below. Examples are omitted.

Source owner: Airbnb. License: [MIT](../LICENSE). Changes by style-skills contributors: rules reworded, shortened and regrouped; examples removed; dated behavior qualified; the syntax-policy citation corrected. Unofficial; no endorsement is implied.

## Tooling

- Under Airbnb's syntax policy, avoid proposals earlier than stage 3; later-stage features still require the guide's individual approval where specified. — [Airbnb: Introduction](https://github.com/airbnb/javascript/tree/master/react). <!-- airbnb-react-jsx:4 -->
- For multiline attributes, indent each attribute on a separate line and align the closing bracket. — [Airbnb: Alignment](https://github.com/airbnb/javascript/tree/master/react#alignment). <!-- airbnb-react-jsx:16 -->
- Nest child JSX one indentation level inside its parent and line up matching start and end tags. — [Airbnb: Alignment](https://github.com/airbnb/javascript/tree/master/react#alignment). <!-- airbnb-react-jsx:17 -->
- A short tag with one attribute, or a suitable short tag without children, may remain on one line. — [Airbnb: Alignment](https://github.com/airbnb/javascript/tree/master/react#alignment). <!-- airbnb-react-jsx:18 -->
- Choose double-quoted JSX attribute strings and single-quoted JavaScript strings. — [Airbnb: Quotes](https://github.com/airbnb/javascript/tree/master/react#quotes). <!-- airbnb-react-jsx:19 -->
- Separate a self-closing slash from the preceding content with one space. — [Airbnb: Spacing](https://github.com/airbnb/javascript/tree/master/react#spacing). <!-- airbnb-react-jsx:20 -->
- Keep JSX expression contents flush against their braces without padding spaces. — [Airbnb: Spacing](https://github.com/airbnb/javascript/tree/master/react#spacing). <!-- airbnb-react-jsx:21 -->
- Enclose a JSX expression in parentheses when it extends across multiple lines. — [Airbnb: Parentheses](https://github.com/airbnb/javascript/tree/master/react#parentheses). <!-- airbnb-react-jsx:34 -->
- Write a self-closing tag when the element has no children. — [Airbnb: Tags](https://github.com/airbnb/javascript/tree/master/react#tags). <!-- airbnb-react-jsx:35 -->
- Move the closing bracket to a separate line if the attributes occupy multiple lines. — [Airbnb: Tags](https://github.com/airbnb/javascript/tree/master/react#tags). <!-- airbnb-react-jsx:36 -->

## Naming

- Spell component filenames and component references in PascalCase. — [Airbnb: Naming](https://github.com/airbnb/javascript/tree/master/react#naming). <!-- airbnb-react-jsx:9 -->
- Spell references to component instances in camelCase. — [Airbnb: Naming](https://github.com/airbnb/javascript/tree/master/react#naming). <!-- airbnb-react-jsx:10 -->
- Give a component the same name as the file that contains it. — [Airbnb: Naming](https://github.com/airbnb/javascript/tree/master/react#naming). <!-- airbnb-react-jsx:11 -->
- For a directory's root component, use `index.jsx` and a component name matching the directory. — [Airbnb: Naming](https://github.com/airbnb/javascript/tree/master/react#naming). <!-- airbnb-react-jsx:12 -->
- Give a higher-order component's result a `displayName` identifying both the wrapper and wrapped component. — [Airbnb: Naming](https://github.com/airbnb/javascript/tree/master/react#naming). <!-- airbnb-react-jsx:13 -->
- Preserve familiar DOM meanings when reusing names such as `className` or `style` as props. — [Airbnb: Naming](https://github.com/airbnb/javascript/tree/master/react#naming). <!-- airbnb-react-jsx:14 -->
- Use the component's reference name as its identity instead of supplying an ordinary component's name through `displayName`. — [Airbnb: Declaration](https://github.com/airbnb/javascript/tree/master/react#declaration). <!-- airbnb-react-jsx:15 -->
- Use camelCase for ordinary prop names and PascalCase for props whose values are components. — [Airbnb: Props](https://github.com/airbnb/javascript/tree/master/react#props). <!-- airbnb-react-jsx:22 -->
- Do not signal an internal component method by adding a leading underscore. — [Airbnb: Methods](https://github.com/airbnb/javascript/tree/master/react#methods). <!-- airbnb-react-jsx:40 -->

## Files and layout

- Default to one component in each file; the guide permits several stateless or pure components together. — [Airbnb: Basic Rules](https://github.com/airbnb/javascript/tree/master/react#basic-rules). <!-- airbnb-react-jsx:1 -->
- Use `.jsx` for JavaScript component files under Airbnb's filename convention. — [Airbnb: Naming](https://github.com/airbnb/javascript/tree/master/react#naming). <!-- airbnb-react-jsx:8 -->
- [dated ordering] In existing ES classes, order static methods, constructor, child-context/pre-mount work, mount, incoming-prop work, update checks/before-and-after callbacks, unmount, handle-handlers, on-handlers, render getters, render helpers, and finally render. — [Airbnb: Ordering](https://github.com/airbnb/javascript/tree/master/react#ordering). <!-- airbnb-react-jsx:42 -->
- [dated APIs] Treat the ordering slots for `getChildContext`, `componentWillMount`, `componentWillReceiveProps`, and `componentWillUpdate` as historical; do not introduce removed or unsafe APIs to fill them. — [Airbnb: Ordering](https://github.com/airbnb/javascript/tree/master/react#ordering). <!-- airbnb-react-jsx:43 -->
- [dated prop validation] The ES-class example places `propTypes` and then `defaultProps` assignments below the class; React 19 ignores `propTypes`, while class `defaultProps` remains supported. — [Airbnb: Ordering](https://github.com/airbnb/javascript/tree/master/react#ordering). <!-- airbnb-react-jsx:44 -->
- [dated createClass] For legacy ordering only, the sequence is displayName, propTypes, contextTypes, childContextTypes, mixins, statics, defaultProps, getDefaultProps, getInitialState, getChildContext, lifecycles, handlers, render getters/helpers, and render. — [Airbnb: Ordering](https://github.com/airbnb/javascript/tree/master/react#ordering). <!-- airbnb-react-jsx:45 -->
- [dated ordering] A mixins position in the historical ordering list does not override the guide's ban on mixins. — [Airbnb: Ordering](https://github.com/airbnb/javascript/tree/master/react#ordering). <!-- airbnb-react-jsx:46 -->

## Types and data

- [dated prop validation] Where legacy prop validation is relevant, describe array element types and object contents explicitly; React 19 no longer checks `propTypes`. — [Airbnb: Basic Rules](https://github.com/airbnb/javascript/tree/master/react#basic-rules). <!-- airbnb-react-jsx:3 -->
- [dated for functions] Airbnb requires defaults for every optional prop through `defaultProps`; for React 19 function components, use parameter defaults instead. — [Airbnb: Props](https://github.com/airbnb/javascript/tree/master/react#props). <!-- airbnb-react-jsx:29 -->
- Use JSX prop spreading selectively instead of making it the normal way to pass every prop. — [Airbnb: Props](https://github.com/airbnb/javascript/tree/master/react#props). <!-- airbnb-react-jsx:30 -->
- Prop forwarding by a higher-order component and spreading an object of explicitly known props are allowed exceptions. — [Airbnb: Props](https://github.com/airbnb/javascript/tree/master/react#props). <!-- airbnb-react-jsx:31 -->
- Remove unrelated props before forwarding; the source's suggestion of exact prop validation applies to legacy validation systems, not React 19 runtime checks. — [Airbnb: Props](https://github.com/airbnb/javascript/tree/master/react#props). <!-- airbnb-react-jsx:32 -->

## Performance

- Arrow closures may capture extra event-local values, but account for the cost of changing callback identity. — [Airbnb: Methods](https://github.com/airbnb/javascript/tree/master/react#methods). <!-- airbnb-react-jsx:37 -->

## Language-specific pitfalls

- Express elements with JSX; reserve `React.createElement` for app initialization in a file without JSX. — [Airbnb: Basic Rules](https://github.com/airbnb/javascript/tree/master/react#basic-rules). <!-- airbnb-react-jsx:2 -->
- [dated state/ref model] Airbnb prefers ES classes over `createClass` for state or refs; modern state and refs do not require a class, so follow official React guidance when choosing new components. — [Airbnb: Class vs React.createClass vs stateless](https://github.com/airbnb/javascript/tree/master/react#class-vs-reactcreateclass-vs-stateless). <!-- airbnb-react-jsx:5 -->
- For the source's stateless, ref-free case, prefer an ordinary named function to a class or arrow component; this historical scope does not exclude Hooks in function components. — [Airbnb: Class vs React.createClass vs stateless](https://github.com/airbnb/javascript/tree/master/react#class-vs-reactcreateclass-vs-stateless). <!-- airbnb-react-jsx:6 -->
- Avoid mixins in component implementations. — [Airbnb: Mixins](https://github.com/airbnb/javascript/tree/master/react#mixins). <!-- airbnb-react-jsx:7 -->
- For a prop whose value is true, use the JSX boolean shorthand without an explicit value. — [Airbnb: Props](https://github.com/airbnb/javascript/tree/master/react#props). <!-- airbnb-react-jsx:23 -->
- Supply image alternative text; Airbnb allows decorative images either an empty `alt` value or a presentation role. — [Airbnb: Props](https://github.com/airbnb/javascript/tree/master/react#props). <!-- airbnb-react-jsx:24 -->
- Describe the image content without redundant image/photo/picture wording in alternative text. — [Airbnb: Props](https://github.com/airbnb/javascript/tree/master/react#props). <!-- airbnb-react-jsx:25 -->
- Select an existing non-abstract ARIA role for an element's `role` attribute. — [Airbnb: Props](https://github.com/airbnb/javascript/tree/master/react#props). <!-- airbnb-react-jsx:26 -->
- Leave `accessKey` unset to avoid conflicting keyboard shortcuts. — [Airbnb: Props](https://github.com/airbnb/javascript/tree/master/react#props). <!-- airbnb-react-jsx:27 -->
- Prefer persistent item identifiers for keys, especially when list positions can change. — [Airbnb: Props](https://github.com/airbnb/javascript/tree/master/react#props). <!-- airbnb-react-jsx:28 -->
- [dated refs] Airbnb's historical ref convention requires callbacks instead of strings; apply official React guidance when object refs or modern ref APIs conflict with that restriction. — [Airbnb: Refs](https://github.com/airbnb/javascript/tree/master/react#refs). <!-- airbnb-react-jsx:33 -->
- For an existing class, bind handlers used during rendering once in its constructor. — [Airbnb: Methods](https://github.com/airbnb/javascript/tree/master/react#methods). <!-- airbnb-react-jsx:38 -->
- Under Airbnb's class-handler convention, avoid defining handlers as arrow-valued class fields. — [Airbnb: Methods](https://github.com/airbnb/javascript/tree/master/react#methods). <!-- airbnb-react-jsx:39 -->
- Ensure a class component's `render` method returns its result. — [Airbnb: Methods](https://github.com/airbnb/javascript/tree/master/react#methods). <!-- airbnb-react-jsx:41 -->
- Do not use the legacy `isMounted` API. — [Airbnb: isMounted](https://github.com/airbnb/javascript/tree/master/react#ismounted). <!-- airbnb-react-jsx:47 -->

## Where the sources disagree

Prefer `react-official-style` where it clashes with this source. For modern component authoring, follow the [official Component guidance](https://react.dev/reference/react/Component): function components can own state and refs. The class and createClass sequences above document historical ordering, not a request to introduce legacy APIs.

The [React 19 upgrade guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide) supersedes runtime `propTypes`, function `defaultProps`, legacy context, and string refs. Use a typing solution and function parameter defaults where relevant; class `defaultProps` is still supported. Read the [current ref documentation](https://react.dev/learn/manipulating-the-dom-with-refs) when Airbnb’s always-callback rule conflicts with the project’s modern ref usage.

Formatting and syntax conventions remain subject to the project’s existing formatter and linter. The syntax-stage restriction is from the introduction, the Introduction section.
