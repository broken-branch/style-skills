# Bulletproof React rules

Bulletproof React architecture guidance, including adaptable source and feature layouts. Demo-specific data models, auth wiring, and workflow examples are omitted.

Source owner: Alan Alickovic. License: [MIT](../LICENSE). Changes by style-skills contributors: rules restated, shortened and regrouped; examples and source-local rules removed; abbreviated section labels expanded. Unofficial; no endorsement is implied.

## Tooling

- Use import restrictions in the linter to check the chosen architectural boundaries. — [Bulletproof React: Project Structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md). <!-- bulletproof-react:8 -->
- Encode agreed project and language conventions in lint checks. — [Bulletproof React: ESLint](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-standards.md). <!-- bulletproof-react:18 -->
- Automate formatting and consider running the formatter when saving files. — [Bulletproof React: Prettier](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-standards.md). <!-- bulletproof-react:19 -->
- Use TypeScript to catch invalid data shapes and mistakes introduced by refactoring. — [Bulletproof React: TypeScript](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-standards.md). <!-- bulletproof-react:20 -->
- Use commit-time hooks for the project's appropriate lint, format, and type checks. — [Bulletproof React: Husky](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-standards.md). <!-- bulletproof-react:23 -->
- Have lint and formatting tools enforce the naming and style choices consistently. — [Bulletproof React: Stay consistent](https://github.com/alan2207/bulletproof-react/blob/master/docs/components-and-styling.md). <!-- bulletproof-react:29 -->

## Naming

- Choose one file/folder naming scheme and enforce it; kebab-case is the source's illustrative choice. — [Bulletproof React: File naming conventions](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-standards.md). <!-- bulletproof-react:26 -->

## Files and layout

- Prefer one `@/*` alias for `src/*` when configuring absolute imports. — [Bulletproof React — Absolute imports](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-standards.md). <!-- bulletproof-react:25 -->

- Within a feature, add only the needed `api`, `assets`, `components`, `hooks`, `stores`, `types`, and `utils` folders. — [Bulletproof React — Feature structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md). <!-- bulletproof-react:17 -->

- Use `src/app`, `assets`, `components`, `config`, `features`, `hooks`, `lib`, `stores`, `testing`, `types`, and `utils` as an adaptable layout. Framework routing may change `app`; shared components, Hooks, libraries, types, and helpers belong in the corresponding shared folders. — [Bulletproof React — Project structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md). <!-- bulletproof-react:9 --> <!-- bulletproof-react:10 --> <!-- bulletproof-react:11 --> <!-- bulletproof-react:12 --> <!-- bulletproof-react:13 --> <!-- bulletproof-react:14 --> <!-- bulletproof-react:15 --> <!-- bulletproof-react:16 -->

- Group most application code into features, separating each feature's implementation from shared support code. — [Bulletproof React: Project Structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md). <!-- bulletproof-react:1 -->
- Add a feature subdirectory only when the feature has code that belongs there. — [Bulletproof React: Project Structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md). <!-- bulletproof-react:2 -->
- A common API directory is an option when several features would otherwise duplicate request definitions. — [Bulletproof React: Project Structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md). <!-- bulletproof-react:3 -->
- Prefer direct imports of implementation files over feature barrels under the source's Vite tree-shaking guidance. — [Bulletproof React: Project Structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md). <!-- bulletproof-react:4 -->
- Prefer assembling features in the app layer instead of coupling them through cross-feature imports. — [Bulletproof React: Project Structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md). <!-- bulletproof-react:5 -->
- Direct imports from app code toward features or shared code, and from features toward shared code. — [Bulletproof React: Project Structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md). <!-- bulletproof-react:6 -->
- Keep app and feature dependencies out of shared modules, and app dependencies out of feature modules. — [Bulletproof React: Project Structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md). <!-- bulletproof-react:7 -->
- Use configured absolute imports to avoid long chains of parent-directory navigation. — [Bulletproof React: Absolute imports](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-standards.md). <!-- bulletproof-react:24 -->
- Place components, utilities, styles, and state close to the code that consumes them. — [Bulletproof React: Colocate things as close as possible to where it's being used](https://github.com/alan2207/bulletproof-react/blob/master/docs/components-and-styling.md). <!-- bulletproof-react:27 -->
- Move a coherent piece of UI into its own component before nested rendering helpers make the parent unwieldy. — [Bulletproof React: Avoid large components with nested rendering functions](https://github.com/alan2207/bulletproof-react/blob/master/docs/components-and-styling.md). <!-- bulletproof-react:28 -->
- When a component's prop interface grows too broad, consider smaller components or composition. — [Bulletproof React: Limit the number of props a component is accepting as input](https://github.com/alan2207/bulletproof-react/blob/master/docs/components-and-styling.md). <!-- bulletproof-react:30 -->
- Wait for concrete repetition before introducing a shared UI abstraction. — [Bulletproof React: Abstract shared components into a component library](https://github.com/alan2207/bulletproof-react/blob/master/docs/components-and-styling.md). <!-- bulletproof-react:31 -->
- In a larger application, collect shared UI components and consider adapters around third-party components to contain future changes. — [Bulletproof React: Abstract shared components into a component library](https://github.com/alan2207/bulletproof-react/blob/master/docs/components-and-styling.md). <!-- bulletproof-react:32 -->
- Consider proven component libraries for complex controls rather than implementing every control yourself. — [Bulletproof React: Component libraries](https://github.com/alan2207/bulletproof-react/blob/master/docs/components-and-styling.md). <!-- bulletproof-react:33 -->
- For a custom design system, consider unstyled components that supply behavior without dictating appearance. — [Bulletproof React: Headless component libraries](https://github.com/alan2207/bulletproof-react/blob/master/docs/components-and-styling.md). <!-- bulletproof-react:34 -->
- Choose styling that fits the application, accounting for Server Components' need for a solution without runtime style generation. — [Bulletproof React: Styling Solutions](https://github.com/alan2207/bulletproof-react/blob/master/docs/components-and-styling.md). <!-- bulletproof-react:35 -->
- Share a configured API client instance across application requests. — [Bulletproof React: Use a Single Instance of the API Client](https://github.com/alan2207/bulletproof-react/blob/master/docs/api-layer.md). <!-- bulletproof-react:37 -->
- Create exported request definitions instead of assembling requests independently throughout the UI. — [Bulletproof React: Define and Export Request Declarations](https://github.com/alan2207/bulletproof-react/blob/master/docs/api-layer.md). <!-- bulletproof-react:38 -->
- Include a fetcher that invokes the endpoint through the shared API client. — [Bulletproof React: Define and Export Request Declarations](https://github.com/alan2207/bulletproof-react/blob/master/docs/api-layer.md). <!-- bulletproof-react:40 -->
- Provide a Hook around the fetcher using a query/cache library to coordinate loading and cached data. — [Bulletproof React: Define and Export Request Declarations](https://github.com/alan2207/bulletproof-react/blob/master/docs/api-layer.md). <!-- bulletproof-react:41 -->

## Types and data

- When refactoring around types, change the declarations first and use type errors to find required code updates. — [Bulletproof React: TypeScript](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-standards.md). <!-- bulletproof-react:21 -->
- Do not assume that successful static type checking prevents runtime errors. — [Bulletproof React: TypeScript](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-standards.md). <!-- bulletproof-react:22 -->
- Keep each request's input/output types and validation schemas beside its declaration. — [Bulletproof React: Define and Export Request Declarations](https://github.com/alan2207/bulletproof-react/blob/master/docs/api-layer.md). <!-- bulletproof-react:39 -->
- Distinguish component, application, server-cache, form, and URL state instead of putting everything in one store. — [Bulletproof React: State Management](https://github.com/alan2207/bulletproof-react/blob/master/docs/state-management.md). <!-- bulletproof-react:42 -->
- Begin with component-local state and lift ownership only when additional consumers require it. — [Bulletproof React: Component State](https://github.com/alan2207/bulletproof-react/blob/master/docs/state-management.md). <!-- bulletproof-react:43 -->
- Choose `useState` for simple independent values and `useReducer` when an action coordinates several state changes. — [Bulletproof React: Component State](https://github.com/alan2207/bulletproof-react/blob/master/docs/state-management.md). <!-- bulletproof-react:44 -->
- Make genuinely application-wide state accessible while leaving other state close to its consumers. — [Bulletproof React: Application State](https://github.com/alan2207/bulletproof-react/blob/master/docs/state-management.md). <!-- bulletproof-react:45 -->
- Prefer a dedicated remote-data cache over treating server responses as ordinary global client state. — [Bulletproof React: Server Cache State](https://github.com/alan2207/bulletproof-react/blob/master/docs/state-management.md). <!-- bulletproof-react:46 -->
- Consider a form library when validation, submission, and error-handling requirements make primitive form code cumbersome. — [Bulletproof React: Form State](https://github.com/alan2207/bulletproof-react/blob/master/docs/state-management.md). <!-- bulletproof-react:47 -->
- Adapt the selected form library behind application-level form and field components. — [Bulletproof React: Form State](https://github.com/alan2207/bulletproof-react/blob/master/docs/state-management.md). <!-- bulletproof-react:48 -->
- Validate client-side form inputs using suitable schemas. — [Bulletproof React: Form State](https://github.com/alan2207/bulletproof-react/blob/master/docs/state-management.md). <!-- bulletproof-react:49 -->
- Represent navigable choices in route/query parameters and access or change them through the router. — [Bulletproof React: URL State](https://github.com/alan2207/bulletproof-react/blob/master/docs/state-management.md). <!-- bulletproof-react:50 -->

## Errors

- Handle API failures centrally, including suitable user messages, reauthentication, or token refresh behavior. — [Bulletproof React: API Errors](https://github.com/alan2207/bulletproof-react/blob/master/docs/error-handling.md). <!-- bulletproof-react:58 -->
- Use error boundaries around meaningful UI regions to keep a failure from replacing the entire application. — [Bulletproof React: In App Errors](https://github.com/alan2207/bulletproof-react/blob/master/docs/error-handling.md). <!-- bulletproof-react:59 -->
- Collect production errors and consider a dedicated reporting service. — [Bulletproof React: Error Tracking](https://github.com/alan2207/bulletproof-react/blob/master/docs/error-handling.md). <!-- bulletproof-react:60 -->
- Provide source maps to error-reporting tooling when they are needed to trace failures back to source code. — [Bulletproof React: Error Tracking](https://github.com/alan2207/bulletproof-react/blob/master/docs/error-handling.md). <!-- bulletproof-react:61 -->

## Comments and docs

- Consider a browsable component catalog that supports developing and inspecting components in isolation. — [Bulletproof React: Storybook](https://github.com/alan2207/bulletproof-react/blob/master/docs/components-and-styling.md). <!-- bulletproof-react:36 -->

## Testing

- Give feature integration tests substantial emphasis instead of depending entirely on isolated unit coverage. — [Bulletproof React: Integration Tests](https://github.com/alan2207/bulletproof-react/blob/master/docs/testing.md). <!-- bulletproof-react:51 -->
- Use focused unit tests for shared utilities, reusable components, and complicated standalone logic. — [Bulletproof React: Unit Tests](https://github.com/alan2207/bulletproof-react/blob/master/docs/testing.md). <!-- bulletproof-react:52 -->
- Cover user journeys that exercise both the browser application and its backend. — [Bulletproof React: E2E](https://github.com/alan2207/bulletproof-react/blob/master/docs/testing.md). <!-- bulletproof-react:53 -->
- Assert behavior through user-visible interactions rather than inspecting private implementation details. — [Bulletproof React: Testing Library](https://github.com/alan2207/bulletproof-react/blob/master/docs/testing.md). <!-- bulletproof-react:54 -->
- Mock API requests at the network boundary instead of replacing fetch internals or scattering hardcoded responses through tests. — [Bulletproof React: MSW](https://github.com/alan2207/bulletproof-react/blob/master/docs/testing.md). <!-- bulletproof-react:56 -->
- Use a working mock API when it helps frontend development proceed and exercises the expected request behavior. — [Bulletproof React: MSW](https://github.com/alan2207/bulletproof-react/blob/master/docs/testing.md). <!-- bulletproof-react:57 -->

## Performance

- Prefer route-sized code chunks so the initial download need not contain every screen. — [Bulletproof React: Code Splitting](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:72 -->
- Avoid tiny code chunks when their additional requests cost more than the deferred downloads save. — [Bulletproof React: Code Splitting](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:73 -->
- Partition global state by its consumers and keep updates near the UI that depends on them. — [Bulletproof React: Component and state optimizations](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:74 -->
- Pass a lazy initializer for expensive initial state rather than recalculating it on every render. — [Bulletproof React: Component and state optimizations](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:75 -->
- Consider state tools with atomic updates when many independently changing elements need tracking. — [Bulletproof React: Component and state optimizations](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:76 -->
- Use Context selectively for infrequently changing values and consider selector-based access for frequent updates. — [Bulletproof React: Component and state optimizations](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:77 -->
- Try moving state ownership or composing components before adding Context or a global store. — [Bulletproof React: Component and state optimizations](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:78 -->
- For frequently updating interfaces, consider generating styles at build time to avoid repeated runtime styling cost. — [Bulletproof React: Component and state optimizations](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:79 -->
- Compose a stateful wrapper with caller-provided children so wrapper-only updates can reuse unrelated child UI. — [Bulletproof React: Children as the most basic optimization](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:80 -->
- Consider deferred loading for images outside the visible viewport. — [Bulletproof React: Image optimizations](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:81 -->
- Choose efficient contemporary image formats to reduce transfer cost. — [Bulletproof React: Image optimizations](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:82 -->
- Offer responsive image candidates appropriate to the client's display dimensions. — [Bulletproof React: Image optimizations](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:83 -->
- Track loading and interaction performance using tools that report relevant web metrics. — [Bulletproof React: Web vitals](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:84 -->
- Prefetch data for likely upcoming navigation when doing so reduces the wait for that destination. — [Bulletproof React: Data prefetching](https://github.com/alan2207/bulletproof-react/blob/master/docs/performance.md). <!-- bulletproof-react:85 -->
- Consider a CDN for delivering deployed application assets. — [Bulletproof React: Deployment](https://github.com/alan2207/bulletproof-react/blob/master/docs/deployment.md). <!-- bulletproof-react:86 -->

## Security

- Enforce resource access on the server; client-side authentication also serves the application's user experience. — [Bulletproof React: Auth](https://github.com/alan2207/bulletproof-react/blob/master/docs/security.md). <!-- bulletproof-react:62 -->
- Under the source's approach, prefer keeping tokens in application memory while recognizing that a reload discards that authentication state. — [Bulletproof React: Authentication](https://github.com/alan2207/bulletproof-react/blob/master/docs/security.md). <!-- bulletproof-react:63 -->
- When persisting tokens, account for their exposure to XSS if browser JavaScript can read the storage. — [Bulletproof React: localStorage vs cookie for storing tokens](https://github.com/alan2207/bulletproof-react/blob/master/docs/security.md). <!-- bulletproof-react:64 -->
- For persistence under this approach, prefer cookies set by the server with `HttpOnly` over JavaScript-readable token storage. — [Bulletproof React: localStorage vs cookie for storing tokens](https://github.com/alan2207/bulletproof-react/blob/master/docs/security.md). <!-- bulletproof-react:65 -->
- Use appropriate sanitization when displaying user-provided content to prevent XSS. — [Bulletproof React: localStorage vs cookie for storing tokens](https://github.com/alan2207/bulletproof-react/blob/master/docs/security.md). <!-- bulletproof-react:67 -->
- Expose authenticated-user data through an application-wide user-state abstraction for components that need it. — [Bulletproof React: Handling user data](https://github.com/alan2207/bulletproof-react/blob/master/docs/security.md). <!-- bulletproof-react:68 -->
- Use roles for broad permissions and resource-specific policies for decisions involving ownership or other context. — [Bulletproof React: Authorization](https://github.com/alan2207/bulletproof-react/blob/master/docs/security.md). <!-- bulletproof-react:70 -->

## Where the sources disagree

No unresolved source conflicts in this adaptation. Treat the architecture as a consistent starting point that may be adapted to the project, not a requirement to reproduce the demo. The documented `shared → features → app` diagram describes availability; import dependencies run in the opposite direction, as the rules above specify.

Tooling examples include legacy ESLint configuration filenames; use the project’s supported configuration format. Named libraries in the original are options, not assurances of current version or React Compiler compatibility. The source’s children-composition optimization applies to unrelated UI during wrapper-local updates, not to all possible child renders.
