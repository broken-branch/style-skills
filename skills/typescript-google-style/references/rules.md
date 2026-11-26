# Google TypeScript: condensed rules

Rules are grouped by topic; each line identifies the original section. Recommendations and permissions retain their source strength. Code examples are omitted.

Google-internal tooling (Apps JSPB imports, Closure annotations, and tsetse/tsec conformance) is omitted. Error-only catch assumptions apply only within code that actually enforces that contract.

## Quick rules

- Read “must” and plain commands as requirements, and “should,” “prefer,” or “avoid” as recommendations. — [Terminology notes](https://google.github.io/styleguide/tsguide.html#terminology-notes).
- Enforce the prose rules rather than incidental stylistic choices in examples. — [Guide notes](https://google.github.io/styleguide/tsguide.html#guide-notes).

## Tooling

- Pass type checking with the compiler version supported by the project. — [Google — typescript compiler](https://google.github.io/styleguide/tsguide.html#typescript-compiler).

- Use ASCII spaces for whitespace other than line terminators, and escape other whitespace inside strings. — [Whitespace characters](https://google.github.io/styleguide/tsguide.html#whitespace-characters).
- Put one empty line between consecutive top-level file sections. — [Source file structure](https://google.github.io/styleguide/tsguide.html#source-file-structure).
- Give each local variable its own declaration statement. — [One variable per declaration](https://google.github.io/styleguide/tsguide.html#one-variable-per-declaration).
- Leave class declarations without a trailing semicolon, but terminate statements that contain class expressions. — [Class declarations](https://google.github.io/styleguide/tsguide.html#class-declarations).
- An empty line immediately inside a class body is optional. — [Class declarations](https://google.github.io/styleguide/tsguide.html#class-declarations).
- Do not insert semicolons between class methods. — [Class method declarations](https://google.github.io/styleguide/tsguide.html#class-method-declarations).
- Separate a method declaration from adjacent declarations with one empty line. — [Class method declarations](https://google.github.io/styleguide/tsguide.html#class-method-declarations).
- Include a parenthesized argument list even when invoking a constructor with no arguments. — [Constructors](https://google.github.io/styleguide/tsguide.html#constructors).
- Leave one empty line between a constructor and neighboring code. — [Constructors](https://google.github.io/styleguide/tsguide.html#constructors).
- Omit `public` except when declaring a public constructor parameter property that is not `readonly`. — [Visibility](https://google.github.io/styleguide/tsguide.html#visibility).
- Keep function-body edges free of empty lines; use internal blank lines sparingly to distinguish logical groups. — [Formatting functions](https://google.github.io/styleguide/tsguide.html#formatting-functions).
- Attach generator stars to `function` or `yield`, and omit whitespace immediately after rest/spread markers. — [Formatting functions](https://google.github.io/styleguide/tsguide.html#formatting-functions).
- Prefer parentheses for a lone arrow parameter, while permitting the unparenthesized form. — [Formatting functions](https://google.github.io/styleguide/tsguide.html#formatting-functions).
- Quote ordinary strings with single quotes, allowing double quotes when they avoid escaping an apostrophe. — [Use single quotes](https://google.github.io/styleguide/tsguide.html#use-single-quotes).
- Do not split string literals with a backslash followed by a source newline. — [No line continuations](https://google.github.io/styleguide/tsguide.html#no-line-continuations).
- Spell numeric base prefixes in lowercase and avoid legacy leading-zero literals. — [Number literals](https://google.github.io/styleguide/tsguide.html#number-literals).
- Put controlled statements in braces, with the first statement of a nonempty block on the next line. — [Control flow statements and blocks](https://google.github.io/styleguide/tsguide.html#control-flow-statements-blocks).
- Only a complete single-line `if` may omit its braces. — [Control flow statements and blocks](https://google.github.io/styleguide/tsguide.html#control-flow-statements-blocks).
- Remove grouping parentheses only when the expression stays unambiguous to a typical reader. — [Grouping parentheses](https://google.github.io/styleguide/tsguide.html#grouping-parentheses).
- Avoid unnecessary parentheses around complete operands of `return`, `throw`, `delete`, `typeof`, `void`, `case`, `in`, `of`, or `yield`. — [Grouping parentheses](https://google.github.io/styleguide/tsguide.html#grouping-parentheses).
- Write type assertions with `as`, avoiding angle-bracket assertion syntax. — [Type assertion syntax](https://google.github.io/styleguide/tsguide.html#type-assertions-syntax).
- Keep decorators directly adjacent to their declarations without intervening blank lines. — [Decorators](https://google.github.io/styleguide/tsguide.html#decorators).
- Terminate statements with explicit semicolons instead of depending on automatic insertion. — [Automatic Semicolon Insertion](https://google.github.io/styleguide/tsguide.html#automatic-semicolon-insertion).
- Do not silence checking with `@ts-ignore`, `@ts-nocheck`, or `@ts-expect-error` in ordinary production code. — [@ts-ignore](https://google.github.io/styleguide/tsguide.html#ts-ignore).
- Avoid blanket reformatting of untouched files; substantial edits should bring the affected file into conformance. — [Reformatting existing code](https://google.github.io/styleguide/tsguide.html#reformatting-existing-code).
- Keep broad incidental style cleanup separate from a focused functional change. — [Reformatting existing code](https://google.github.io/styleguide/tsguide.html#reformatting-existing-code).
- Generated formatting is exempt, but generated names exposed to handwritten code follow naming conventions with an underscore exception. — [Generated code: mostly exempt](https://google.github.io/styleguide/tsguide.html#generated-code).
- Prefer machine-enforced checks so human review can focus on substantive design and correctness. — [Style guide goals](https://google.github.io/styleguide/tsguide.html#style-guide-goals).

## Naming

- Limit identifiers to ASCII characters; reserve underscores for constants and structured test names, and use dollar signs rarely. — [Identifiers](https://google.github.io/styleguide/tsguide.html#identifiers).
- Avoid type-encoding prefixes and underscore-based privacy markers in names. — [Naming style](https://google.github.io/styleguide/tsguide.html#naming-style).
- Do not mark optional parameters with `opt_`, or interfaces with `I` or redundant `Interface`, except when the environment requires it. — [Naming style](https://google.github.io/styleguide/tsguide.html#naming-style).
- Name an interface for its contract or role rather than merely after its implementing class. — [Naming style](https://google.github.io/styleguide/tsguide.html#naming-style).
- A team may consistently use a dollar suffix for Observable bindings. — [Naming style](https://google.github.io/styleguide/tsguide.html#naming-style).
- Choose descriptive words instead of obscure abbreviations or shortened spellings with missing letters. — [Descriptive names](https://google.github.io/styleguide/tsguide.html#descriptive-names).
- Short names are acceptable for unexported bindings whose visible scope spans at most ten lines. — [Descriptive names](https://google.github.io/styleguide/tsguide.html#descriptive-names).
- Camel-case acronyms like ordinary words, preserving a platform's spelling when compatibility requires it. — [Camel case](https://google.github.io/styleguide/tsguide.html#camel-case).
- Avoid `$` unless following a relevant framework or Observable naming convention. — [Dollar sign](https://google.github.io/styleguide/tsguide.html#identifiers-dollar-sign).
- Prefer UpperCamelCase for type declarations, enums, decorators, type parameters, and TSX component functions. — [Rules by identifier type](https://google.github.io/styleguide/tsguide.html#naming-rules-by-identifier-type).
- Prefer lowerCamelCase for variables, parameters, ordinary functions, methods, properties, and module aliases. — [Rules by identifier type](https://google.github.io/styleguide/tsguide.html#naming-rules-by-identifier-type).
- Prefer CONSTANT_CASE for global constants and module-level enum values, subject to the constant-lifetime rules. — [Rules by identifier type](https://google.github.io/styleguide/tsguide.html#naming-rules-by-identifier-type).
- Name a type parameter with one capital letter or a descriptive UpperCamelCase identifier. — [Type parameters](https://google.github.io/styleguide/tsguide.html#identifiers-type-parameters).
- Use an initial underscore only when syntax requires an unused binding, and prefer an explanatory name after it. — [Underscore (`_`) prefix/suffix](https://google.github.io/styleguide/tsguide.html#identifiers-underscore-prefix-suffix).
- Remove unused parameters at the end of a signature, except on methods designed for overriding. — [Underscore (`_`) prefix/suffix](https://google.github.io/styleguide/tsguide.html#identifiers-underscore-prefix-suffix).
- Do not append underscores to identifier names. — [Underscore (`_`) prefix/suffix](https://google.github.io/styleguide/tsguide.html#identifiers-underscore-prefix-suffix).
- Use lowerCamelCase for namespace imports even if the imported filename uses snake_case. — [Imports](https://google.github.io/styleguide/tsguide.html#identifiers-imports).
- The established jQuery `$` and three.js `THREE` namespace aliases are permitted exceptions. — [Imports](https://google.github.io/styleguide/tsguide.html#identifiers-imports).
- Reserve CONSTANT_CASE for intentionally stable module/global-lifetime values, including static readonly fields of module-level classes. — [Constants](https://google.github.io/styleguide/tsguide.html#identifiers-constants).
- Use lowerCamelCase for locals and values created repeatedly, except aliases preserving an existing symbol's spelling. — [Constants](https://google.github.io/styleguide/tsguide.html#identifiers-constants).
- An arrow function implementing an interface may keep a lowerCamelCase binding. — [Constants](https://google.github.io/styleguide/tsguide.html#identifiers-constants).
- Preserve a locally aliased symbol's spelling and capitalization, declaring the alias with `const` or a `readonly` field. — [Aliases](https://google.github.io/styleguide/tsguide.html#aliases).
- Give an index signature's key parameter a label describing the keys it represents. — [Indexable types / index signatures (`{[key: string]: T}`)](https://google.github.io/styleguide/tsguide.html#indexable-key-string-type).

## Files and layout

- Save source text using UTF-8 encoding. — [File encoding: UTF-8](https://google.github.io/styleguide/tsguide.html#file-encoding-utf-8).
- Arrange each file as copyright notice, file overview, imports, and implementation, omitting optional sections when unnecessary. — [Source file structure](https://google.github.io/styleguide/tsguide.html#source-file-structure).
- Import TypeScript dependencies using named bindings or a namespace binding. — [Imports](https://google.github.io/styleguide/tsguide.html#imports).
- Reserve default imports for external APIs that require that form. — [Imports](https://google.github.io/styleguide/tsguide.html#imports).
- Use a binding-free import when loading a dependency specifically for its side effects. — [Imports](https://google.github.io/styleguide/tsguide.html#imports).
- Identify TypeScript imports with module paths. — [Import paths](https://google.github.io/styleguide/tsguide.html#import-paths).
- Favor relative imports within a logical project, without long chains of parent-directory segments. — [Import paths](https://google.github.io/styleguide/tsguide.html#import-paths).
- Favor named imports for common symbols or names that already explain their meaning. — [Namespace versus named imports](https://google.github.io/styleguide/tsguide.html#namespace-versus-named-imports).
- Favor namespace imports for broad use of a large API or when a qualifier makes generic names clearer. — [Namespace versus named imports](https://google.github.io/styleguide/tsguide.html#namespace-versus-named-imports).
- First consider a namespace or a better export name for collisions; rename an import when that makes its use clearer. — [Renaming imports](https://google.github.io/styleguide/tsguide.html#renaming-imports).
- Expose named exports; do not introduce a default export. — [Exports](https://google.github.io/styleguide/tsguide.html#exports).
- Let the module itself provide the namespace instead of exporting a large wrapper object. — [Exports](https://google.github.io/styleguide/tsguide.html#exports).
- Keep exports limited to the symbols other modules actually need. — [Export visibility](https://google.github.io/styleguide/tsguide.html#export-visibility).
- Do not expose a reassignable binding through `export let`. — [Mutable exports](https://google.github.io/styleguide/tsguide.html#mutable-exports).
- Provide explicit getter/setter functions when consumers must interact with shared mutable state. — [Mutable exports](https://google.github.io/styleguide/tsguide.html#mutable-exports).
- Resolve any conditional choice of export while the module initializes. — [Mutable exports](https://google.github.io/styleguide/tsguide.html#mutable-exports).
- Do not use a class containing only static members as a namespace. — [Container classes](https://google.github.io/styleguide/tsguide.html#container-classes).
- Type-only dependencies may use `import type`; runtime dependencies need ordinary value imports. — [Import type](https://google.github.io/styleguide/tsguide.html#import-type).
- If a dependency must execute at load time, express that with a separate side-effect import. — [Import type](https://google.github.io/styleguide/tsguide.html#import-type).
- Re-export types with the `export type` form. — [Export type](https://google.github.io/styleguide/tsguide.html#export-type).
- When type and value consumers need genuinely separate APIs, give them separate exported symbols. — [Export type](https://google.github.io/styleguide/tsguide.html#export-type).
- Use declared type imports instead of `import()` embedded in a type expression. — [Dynamic `import()` type](https://google.github.io/styleguide/tsguide.html#dynamic-import-type).
- Structure code across files with ECMAScript modules, not TypeScript namespaces or legacy internal modules. — [Use modules not namespaces](https://google.github.io/styleguide/tsguide.html#use-modules-not-namespaces).
- A namespace is permitted when interoperability with an external dependency requires it. — [Use modules not namespaces](https://google.github.io/styleguide/tsguide.html#use-modules-not-namespaces).
- Use ES module syntax instead of `require` or import-equals declarations. — [Use modules not namespaces](https://google.github.io/styleguide/tsguide.html#use-modules-not-namespaces).
- Prefer a private module function to a private static method when it remains easy to read. — [Avoid private static methods](https://google.github.io/styleguide/tsguide.html#avoid-private-static-methods).
- Keep functions cohesive; around forty lines or difficult nesting, debugging, or mixed responsibilities should prompt reconsidering decomposition, not an automatic size violation. — [Function Length](https://google.github.io/styleguide/tsguide.html#function-length).
- Add names to the global object only when integrating with an API that requires them. — [Modifying built-in objects](https://google.github.io/styleguide/tsguide.html#modifying-builtin-objects).

## Types and data

- Angular template-only access is an exception to the restriction on accessing private class properties outside the class body. — [Google — properties used outside of class lexical scope](https://google.github.io/styleguide/tsguide.html#properties-used-outside-of-class-lexical-scope).

- Avoid `{}` as a type; choose `unknown`, `Record`, or `object` to express the intended domain. — [Google — empty interface type](https://google.github.io/styleguide/tsguide.html#empty-interface-type).

- Use TypeScript `private` rather than JavaScript `#private` fields; Google cites downlevel output size and adequate static checking. — [Google — no private fields](https://google.github.io/styleguide/tsguide.html#no-private-fields).

- Choose a character's standard named escape when available; reject legacy octal escapes. — [Special escape sequences](https://google.github.io/styleguide/tsguide.html#special-escape-sequences).
- Write readable Unicode directly; escapes for invisible characters may carry an explanatory comment. — [Non-ASCII characters](https://google.github.io/styleguide/tsguide.html#non-ascii-characters).
- Declare bindings with `const`, switching to `let` for reassignment; omit `var` entirely. — [Use const and let](https://google.github.io/styleguide/tsguide.html#use-const-and-let).
- Build arrays with literal syntax or `Array.from`, avoiding the overloaded `Array` constructor. — [Do not use the `Array` constructor](https://google.github.io/styleguide/tsguide.html#array-constructor).
- Store dictionary entries in an object or map, not arbitrary named array properties; `length` is exempt. — [Do not define properties on arrays](https://google.github.io/styleguide/tsguide.html#do-not-define-properties-on-arrays).
- Skip unused positions in array destructuring, and keep a rest binding against its `...` marker. — [Array destructuring](https://google.github.io/styleguide/tsguide.html#array-destructuring).
- For an optional destructured array argument, default the argument to an empty array and default elements inside the pattern. — [Array destructuring](https://google.github.io/styleguide/tsguide.html#array-destructuring).
- Prefer named object fields over positional arrays when passing or returning heterogeneous data. — [Array destructuring](https://google.github.io/styleguide/tsguide.html#array-destructuring).
- Construct ordinary objects with literals, not calls to `Object`. — [Do not use the `Object` constructor](https://google.github.io/styleguide/tsguide.html#object-constructor).
- Object spread may make shallow copies; remember that a later occurrence of a property replaces its earlier value. — [Using spread syntax](https://google.github.io/styleguide/tsguide.html#object-spread-syntax).
- Treat computed string keys as dictionary keys, keeping them separate from unquoted structural property names. — [Computed property names](https://google.github.io/styleguide/tsguide.html#computed-property-names).
- Limit destructured parameters to a single level of unquoted shorthand properties, with no nested patterns or computed keys. — [Object destructuring](https://google.github.io/styleguide/tsguide.html#object-destructuring).
- Place defaults inside object destructuring, and give an optional destructured object parameter an empty-object default. — [Object destructuring](https://google.github.io/styleguide/tsguide.html#object-destructuring).
- Keep values needed only during construction in local variables instead of instance fields. — [Don't create member variables only used in constructors](https://google.github.io/styleguide/tsguide.html#no-ctor-only-members).
- Remove constructors that merely repeat the language's implicit empty or forwarding behavior. — [Constructors](https://google.github.io/styleguide/tsguide.html#constructors).
- Keep an empty constructor when its parameter properties, access level, or parameter decorators have a purpose. — [Constructors](https://google.github.io/styleguide/tsguide.html#constructors).
- Add `readonly` to fields whose bindings stay fixed after construction. — [Use readonly](https://google.github.io/styleguide/tsguide.html#use-readonly).
- Use parameter properties when constructor arguments are simply assigned to corresponding fields. — [Parameter properties](https://google.github.io/styleguide/tsguide.html#parameter-properties).
- Initialize fields at their declarations when no constructor argument is needed for the value. — [Field initializers](https://google.github.io/styleguide/tsguide.html#field-initializers).
- A property accessed beyond the defining class's lexical boundary must not be declared private. — [Properties used outside of class lexical scope](https://google.github.io/styleguide/tsguide.html#properties-used-outside-of-class-lexical-scope).
- Respect visibility modifiers instead of circumventing them through string-key indexing. — [Properties used outside of class lexical scope](https://google.github.io/styleguide/tsguide.html#properties-used-outside-of-class-lexical-scope).
- Make getters repeatable and free of observable side effects. — [Getters and setters](https://google.github.io/styleguide/tsguide.html#classes-getters-and-setters).
- Expose a field directly, possibly as `readonly`, instead of surrounding it with trivial accessors. — [Getters and setters](https://google.github.io/styleguide/tsguide.html#classes-getters-and-setters).
- Prefer using an accessor even internally when practical, and give its backing field a meaningful whole-word name. — [Getters and setters](https://google.github.io/styleguide/tsguide.html#classes-getters-and-setters).
- Declare accessors with language syntax rather than `Object.defineProperty`. — [Getters and setters](https://google.github.io/styleguide/tsguide.html#classes-getters-and-setters).
- Use computed class member names only when their keys are symbols. — [Computed properties](https://google.github.io/styleguide/tsguide.html#class-computed-properties).
- Give iterable classes a `Symbol.iterator`; use other symbol hooks cautiously and check runtime support. — [Computed properties](https://google.github.io/styleguide/tsguide.html#class-computed-properties).
- Choose the narrowest useful member visibility and consider a module helper instead of a private method. — [Visibility](https://google.github.io/styleguide/tsguide.html#visibility).
- Avoid direct prototype manipulation and prototype-changing mixins in application code. — [Do not manipulate `prototype`s directly](https://google.github.io/styleguide/tsguide.html#class-prototypes).
- Leave built-in prototypes unchanged. — [Do not manipulate `prototype`s directly](https://google.github.io/styleguide/tsguide.html#class-prototypes).
- Framework internals may manipulate prototypes when alternatives would create worse workarounds. — [Do not manipulate `prototype`s directly](https://google.github.io/styleguide/tsguide.html#class-prototypes).
- Prefer declarations for named functions; an arrow is acceptable when an explicit function type is needed. — [Prefer function declarations for named functions](https://google.github.io/styleguide/tsguide.html#function-declarations).
- Nested functions may be declarations or arrows; favor arrows inside methods when lexical `this` is useful. — [Nested functions](https://google.github.io/styleguide/tsguide.html#nested-functions).
- Prefer arrows to function expressions, retaining expressions for generators or intentional `this` rebinding. — [Do not use function expressions](https://google.github.io/styleguide/tsguide.html#function-expressions).
- Choose an arrow body to suit the task, using expression bodies only when their returned value is used. — [Arrow function bodies](https://google.github.io/styleguide/tsguide.html#arrow-function-bodies).
- Use a block body or a `void` expression for a callback whose result should be ignored. — [Arrow function bodies](https://google.github.io/styleguide/tsguide.html#arrow-function-bodies).
- Prefer lexical arrows or explicit parameters over `bind`, saved receiver variables, and other rebinding mechanisms. — [Rebinding `this`](https://google.github.io/styleguide/tsguide.html#rebinding-this).
- An arrow-function property is acceptable when it substantially simplifies template or framework binding. — [Arrow functions as properties](https://google.github.io/styleguide/tsguide.html#arrow-functions-as-properties).
- Use a persistent arrow property for a receiver-bound event handler that must later be removed. — [Event handlers](https://google.github.io/styleguide/tsguide.html#event-handlers).
- Keep parameter defaults straightforward and avoid visible side effects during their evaluation. — [Parameter initializers](https://google.github.io/styleguide/tsguide.html#parameter-initializers).
- Use default parameters sparingly; prefer a destructured options object for several independent optional settings. — [Parameter initializers](https://google.github.io/styleguide/tsguide.html#parameter-initializers).
- Collect extra arguments with a rest parameter; neither use nor shadow the `arguments` object. — [Prefer rest and spread when appropriate](https://google.github.io/styleguide/tsguide.html#rest-and-spread).
- Expand arguments with spread syntax instead of calling `Function.prototype.apply`. — [Prefer rest and spread when appropriate](https://google.github.io/styleguide/tsguide.html#rest-and-spread).
- Use template interpolation instead of complex string concatenation. — [Template literals](https://google.github.io/styleguide/tsguide.html#template-literals).
- Explicit conversions may use `String`, `Boolean`, interpolation, or double negation, but must not allocate boxed primitives. — [Type coercion](https://google.github.io/styleguide/tsguide.html#type-coercion).
- Test enum values with comparisons instead of explicit Boolean conversion. — [Type coercion](https://google.github.io/styleguide/tsguide.html#type-coercion).
- Avoid using concatenation with an empty string as a conversion operator. — [Type coercion](https://google.github.io/styleguide/tsguide.html#type-coercion).
- Coerce numeric strings with `Number` rather than unary `+` or `parseFloat`. — [Coercing to numbers](https://google.github.io/styleguide/tsguide.html#coercing-to-numbers).
- Reserve `parseInt` for a necessary nondecimal base; first validate every digit and still reject a `NaN` result. — [Coercing to numbers](https://google.github.io/styleguide/tsguide.html#coercing-to-numbers).
- Skip redundant Boolean conversion in conditions of `if`, `for`, and `while`. — [Implicit coercion](https://google.github.io/styleguide/tsguide.html#implicit-coercion).
- Favor `for-of` when traversing arrays; indexed loops and `forEach` are also permitted. — [Iterating containers](https://google.github.io/styleguide/tsguide.html#iterating-containers).
- Prefer `for-of` over `Object.keys`, `Object.values`, or `Object.entries` to dictionary `for-in` loops. — [Iterating containers](https://google.github.io/styleguide/tsguide.html#iterating-containers).
- End every switch with a `default` group, even when that group has no statements. — [Switch statements](https://google.github.io/styleguide/tsguide.html#switch-statements).
- Use strict equality operators, allowing a loose comparison with `null` when intentionally testing both missing-value forms. — [Equality checks](https://google.github.io/styleguide/tsguide.html#equality-checks).
- Prefer runtime narrowing to assertions; retain an assertion only when its safety is apparent or documented. — [Type and non-nullability assertions](https://google.github.io/styleguide/tsguide.html#type-and-non-nullability-assertions).
- For a necessary, justified double assertion, use `unknown` as the intermediate type rather than `any` or `{}`. — [Double assertions](https://google.github.io/styleguide/tsguide.html#double-assertions).
- Type an object literal through a declaration annotation instead of an assertion so missing members remain detectable. — [Type assertions and object literals](https://google.github.io/styleguide/tsguide.html#type-assertions-and-object-literals).
- Do not instantiate `String`, `Number`, or `Boolean` wrapper objects. — [Wrapper objects for primitive types](https://google.github.io/styleguide/tsguide.html#primitive-types-wrapper-classes).
- Declare ordinary enums rather than `const enum`. — [Const enums](https://google.github.io/styleguide/tsguide.html#enums).
- Inference is permitted throughout; omit trivial primitive annotations for unexported locals and defaulted parameters. — [Type inference](https://google.github.io/styleguide/tsguide.html#type-inference).
- Keep exported annotations needed to support `isolatedDeclarations` output. — [Type inference](https://google.github.io/styleguide/tsguide.html#type-inference).
- Omit generic arguments that repeat information already supplied by a type annotation. — [Type inference](https://google.github.io/styleguide/tsguide.html#type-inference).
- Annotate a complicated expression when it improves clarity; leave borderline decisions to review. — [Type inference](https://google.github.io/styleguide/tsguide.html#type-inference).
- Return annotations are normally an author choice, subject to reviewer requests for complex cases and explicit project policy. — [Return types](https://google.github.io/styleguide/tsguide.html#return-types).
- Follow the API's existing convention for `null` versus `undefined`; neither is universally preferred. — [Undefined and null](https://google.github.io/styleguide/tsguide.html#undefined-and-null).
- Add nullability at the point of use rather than inside aliases, and resolve absent values close to where they arise. — [Nullable/undefined type aliases](https://google.github.io/styleguide/tsguide.html#nullableundefined-type-aliases).
- Annotate a structural implementation where it is declared so incompatible shapes fail at their origin. — [Use structural types](https://google.github.io/styleguide/tsguide.html#use-structural-types).
- Model purely structural contracts with interfaces instead of runtime classes. — [Use structural types](https://google.github.io/styleguide/tsguide.html#use-structural-types).
- Prefer interfaces to object-shaped type aliases whenever an interface can represent the contract. — [Prefer interfaces over type literal aliases](https://google.github.io/styleguide/tsguide.html#prefer-interfaces).
- Use `T[]` or `readonly T[]` for simple names and `T[][]` for mutable multidimensional arrays of simple types; use generic array notation for more complex types, applying these choices at each nesting level. — [`Array<T>` Type](https://google.github.io/styleguide/tsguide.html#arrayt-type).
- Consider `Map` or `Set` instead of objects used as associative collections. — [Indexable types / index signatures (`{[key: string]: T}`)](https://google.github.io/styleguide/tsguide.html#indexable-key-string-type).
- Choose straightforward type definitions, accepting some repetition before introducing intricate mapped or conditional types. — [Mapped and conditional types](https://google.github.io/styleguide/tsguide.html#mapped-conditional-types).
- Use mapped or conditional types only when their benefit outweighs readability, tooling, and compatibility costs. — [Mapped and conditional types](https://google.github.io/styleguide/tsguide.html#mapped-conditional-types).
- Avoid `any` where a concrete type, `unknown`, or a justified narrowly scoped suppression serves the need. — [`any` Type](https://google.github.io/styleguide/tsguide.html#any).
- Express known data with a concrete interface, object shape, or alias instead of `any`. — [Providing a more specific type](https://google.github.io/styleguide/tsguide.html#any-specific).
- Represent opaque inputs as `unknown` and narrow them before performing type-specific operations. — [Using `unknown` over `any`](https://google.github.io/styleguide/tsguide.html#any-unknown).
- Prefer a tuple to a generic pair abstraction, but use an object when descriptive field names improve understanding. — [Tuple types](https://google.github.io/styleguide/tsguide.html#tuple-types).
- Use primitive lowercase type names instead of the capitalized wrapper types. — [Wrapper types](https://google.github.io/styleguide/tsguide.html#wrapper-types).
- Avoid declaring generics that occur only in return types; provide an explicit type argument when consuming an existing API of that form. — [Return type only generics](https://google.github.io/styleguide/tsguide.html#return-type-only-generics).

## Errors

- Ensure `toString` cannot fail or produce externally observable side effects. — [Overriding toString](https://google.github.io/styleguide/tsguide.html#overriding-tostring).
- Validate numeric conversion results, including `NaN`, because malformed input need not throw. — [Coercing to numbers](https://google.github.io/styleguide/tsguide.html#coercing-to-numbers).
- Prefer exceptions for exceptional failures and custom types derived from `Error` when useful. — [Exception handling](https://google.github.io/styleguide/tsguide.html#exception-handling).
- Prefer exceptions over invented error-result wrappers or special error properties on return values. — [Exception handling](https://google.github.io/styleguide/tsguide.html#exception-handling).
- Instantiate failures with `new Error` rather than calling `Error` without `new`. — [Instantiate errors using `new`](https://google.github.io/styleguide/tsguide.html#instantiate-errors-using-new).
- Supply `Error` objects to throws, promise rejections, and aborts; a no-argument abort may create its built-in default error. — [Only throw errors](https://google.github.io/styleguide/tsguide.html#only-throw-errors).
- Within an enforced Error-only boundary, special handling of non-Error throws requires a known violating API and a comment identifying it; do not infer that boundary for an external project. — [Catching and rethrowing](https://google.github.io/styleguide/tsguide.html#catching-and-rethrowing).
- An intentionally empty catch needs a comment explaining why ignoring the failure is correct. — [Empty catch blocks](https://google.github.io/styleguide/tsguide.html#empty-catch-blocks).
- Set an error's `cause` to an `Error` instance rather than unrelated data or text. — [ErrorOptions cause must be an Error object](https://google.github.io/styleguide/tsguide.html#error-cause).
- Wrap the original failure in an options object's `cause` field instead of passing the failure itself as `ErrorOptions`. — [ErrorOptions cause must be an Error object](https://google.github.io/styleguide/tsguide.html#error-cause).
- Keep a try block limited to the throwing work it handles when readable; wrapping an entire loop is acceptable for performance. — [Keep try blocks focused](https://google.github.io/styleguide/tsguide.html#keep-try-blocks-focused).

## Comments and docs

- When a copyright or license notice is required, put it in JSDoc at the file's start. — [Copyright information](https://google.github.io/styleguide/tsguide.html#file-copyright).
- A file-level overview may explain purpose, usage, or dependencies; leave its continuation lines unindented. — [`@fileoverview` JSDoc](https://google.github.io/styleguide/tsguide.html#fileoverview).
- Explain a parameter property through an `@param` tag when its meaning needs documentation. — [Parameter properties](https://google.github.io/styleguide/tsguide.html#parameter-properties).
- Document the safety argument for an assertion when the surrounding code does not make it clear. — [Type and non-nullability assertions](https://google.github.io/styleguide/tsguide.html#type-and-non-nullability-assertions).
- Explain the reason for any unavoidable `any` and its associated lint suppression, including deliberate test doubles. — [Suppressing `any` lint warnings](https://google.github.io/styleguide/tsguide.html#any-suppress).
- Use JSDoc for consumers of an API and ordinary line comments for implementation reasoning. — [JSDoc versus comments](https://google.github.io/styleguide/tsguide.html#jsdoc-vs-comments).
- Express multiline implementation notes with aligned `//` lines, avoiding block comments and decorative borders. — [Multi-line comments](https://google.github.io/styleguide/tsguide.html#multi-line-comments).
- Use valid JSDoc syntax, giving multiline comments separate opening and closing delimiter lines. — [JSDoc general form](https://google.github.io/styleguide/tsguide.html#jsdoc-general-form).
- Structure JSDoc with Markdown, adding HTML when necessary. — [Markdown](https://google.github.io/styleguide/tsguide.html#jsdoc-markdown).
- Use recognized JSDoc tags and normally start each on a separate line. — [JSDoc tags](https://google.github.io/styleguide/tsguide.html#jsdoc-tags).
- Indent tag continuations by four spaces without alignment padding; leave `@desc` and `@fileoverview` continuations unindented. — [Line wrapping](https://google.github.io/styleguide/tsguide.html#jsdoc-line-wrapping).
- Explain top-level exports and unclear members without merely restating their identifiers or types. — [Document all top-level exports of modules](https://google.github.io/styleguide/tsguide.html#document-all-top-level-exports-of-modules).
- Documentation may be omitted for framework-obvious symbols exported only for tools to consume. — [Document all top-level exports of modules](https://google.github.io/styleguide/tsguide.html#document-all-top-level-exports-of-modules).
- Describe a class's intended use and correctness constraints; its constructor need not duplicate that explanation. — [Class comments](https://google.github.io/styleguide/tsguide.html#jsdoc-class-comments).
- Start method documentation with a third-person action verb, omitting parameter and return explanations already obvious from the signature. — [Method and function comments](https://google.github.io/styleguide/tsguide.html#method-and-function-comments).
- Describe the field created by a constructor parameter property in that parameter's `@param` documentation. — [Parameter property comments](https://google.github.io/styleguide/tsguide.html#parameter-property-comments).
- Leave types and language modifiers to TypeScript rather than repeating them in JSDoc type, implements, private, or override tags. — [JSDoc type annotations](https://google.github.io/styleguide/tsguide.html#jsdoc-type-annotations).
- Retain `@param` and return tags only when they contribute information beyond the declaration. — [Make comments that actually add information](https://google.github.io/styleguide/tsguide.html#redundant-comments).
- Prefer an options interface or destructuring for unclear arguments; otherwise precede the argument with a parameter-name-equals comment. — [Comments when calling a function](https://google.github.io/styleguide/tsguide.html#comments-when-calling-a-function).
- Existing trailing parameter comments may be retained to match the rest of their file. — [Comments when calling a function](https://google.github.io/styleguide/tsguide.html#comments-when-calling-a-function).
- Place documentation above any decorators rather than between decorators and the declaration. — [Place documentation prior to decorators](https://google.github.io/styleguide/tsguide.html#place-documentation-prior-to-decorators).
- An `@deprecated` tag must explain the migration path clearly. — [Deprecation](https://google.github.io/styleguide/tsguide.html#deprecation).

## Testing

- Use an assertion designed for expected exceptions instead of a try/catch that might swallow the test's own failure. — [Empty catch blocks](https://google.github.io/styleguide/tsguide.html#empty-catch-blocks).
- Underscores may separate the descriptive parts of xUnit-style test method names. — [Test names](https://google.github.io/styleguide/tsguide.html#identifiers-test-names).
- Tests may use `@ts-expect-error` reluctantly; prefer a justified expression-level assertion or a narrowly targeted lint suppression. — [@ts-ignore](https://google.github.io/styleguide/tsguide.html#ts-ignore).

## Performance

- Prefer initializing fields to `undefined` so an instance keeps the same set of fields throughout its lifetime. — [Field initializers](https://google.github.io/styleguide/tsguide.html#field-initializers).
- Normally define methods on the prototype rather than allocating arrow-function properties per instance. — [Arrow functions as properties](https://google.github.io/styleguide/tsguide.html#arrow-functions-as-properties).

## Security

- Avoid evaluating strings through `eval` or `Function`, except when implementing a genuine code loader. — [Dynamic code evaluation](https://google.github.io/styleguide/tsguide.html#dynamic-code-evaluation).

## Language-specific pitfalls

- Do not create decorators; use only the framework-provided decorators the guide permits. — [Google — decorators](https://google.github.io/styleguide/tsguide.html#decorators).

- Declare a variable before referring to it. — [Use const and let](https://google.github.io/styleguide/tsguide.html#use-const-and-let).
- Filter inherited properties out of `for-in`, or enumerate the object's own keys with `Object.keys`. — [Iterating objects](https://google.github.io/styleguide/tsguide.html#iterating-objects).
- Avoid spreading instances, functions, and other objects whose prototype carries behavior. — [Using spread syntax](https://google.github.io/styleguide/tsguide.html#object-spread-syntax).
- Invoke static methods through their declaring class instead of depending on polymorphic dispatch. — [Do not rely on dynamic dispatch](https://google.github.io/styleguide/tsguide.html#avoid-static-method-dynamic-dispatch).
- Avoid `this` references in static code. — [Avoid static `this` references](https://google.github.io/styleguide/tsguide.html#static-this).
- Avoid reading parameter properties from field initializers because native class-field ordering initializes those properties later. — [Field initializers](https://google.github.io/styleguide/tsguide.html#field-initializers).
- An ordinary function may use `this` only when explicitly designed for receiver rebinding. — [Rebinding `this`](https://google.github.io/styleguide/tsguide.html#rebinding-this).
- Prefer an arrow that forwards selected callback arguments, preventing incidental arguments from filling optional parameters. — [Prefer passing arrow functions as callbacks](https://google.github.io/styleguide/tsguide.html#functions-as-callbacks).
- Forward a method invocation through an arrow when passing a callback, preserving its receiver. — [Arrow functions as properties](https://google.github.io/styleguide/tsguide.html#arrow-functions-as-properties).
- Do not bind a fresh temporary listener inline if removal requires the original function identity. — [Event handlers](https://google.github.io/styleguide/tsguide.html#event-handlers).
- Use `this` only in class methods/constructors, functions with a declared `this` type, or arrows nested in such scopes. — [this](https://google.github.io/styleguide/tsguide.html#features-this).
- Do not use `this` as an implicit global, eval context, event target, or unnecessary `call`/`apply` receiver. — [this](https://google.github.io/styleguide/tsguide.html#features-this).
- Compare enum values explicitly in conditions, including values whose union type contains an enum. — [Implicit coercion](https://google.github.io/styleguide/tsguide.html#implicit-coercion).
- Avoid assigning inside a condition; enclose an intentional assignment in an additional pair of parentheses. — [Assignment in control statements](https://google.github.io/styleguide/tsguide.html#assignment-in-control-statements).
- Never traverse an array with `for-in`; for dictionaries, exclude inherited entries. — [Iterating containers](https://google.github.io/styleguide/tsguide.html#iterating-containers).
- End nonempty switch groups with `break`, `return`, or a throw; fallthrough is limited to empty groups. — [Switch statements](https://google.github.io/styleguide/tsguide.html#switch-statements).
- Remove `debugger` statements from production code. — [Debugger statements](https://google.github.io/styleguide/tsguide.html#debugger-statements).
- Exclude the `with` statement from code. — [`with`](https://google.github.io/styleguide/tsguide.html#diallowed-features-with).
- Avoid obsolete features, nonstandard extensions, and language or web proposals that are still unfinished. — [Non-standard features](https://google.github.io/styleguide/tsguide.html#non-standard-features).
- Runtime-specific APIs are acceptable for an intentionally limited target; consider portable wrappers for proprietary APIs. — [Non-standard features](https://google.github.io/styleguide/tsguide.html#non-standard-features).
- Do not extend built-in objects or adopt dependencies that require such extensions. — [Modifying built-in objects](https://google.github.io/styleguide/tsguide.html#modifying-builtin-objects).

## Where the sources disagree

- For a choice this guide leaves open, follow the file's convention first and nearby files second. — [Consistency](https://google.github.io/styleguide/tsguide.html#consistency).
- Use current style for new files and satisfy mandatory rules when adding code to older files. — [Consistency](https://google.github.io/styleguide/tsguide.html#consistency).
- Keep context-sensitive choices local unless a global rule prevents known trouble, removes pointless variation, or benefits long-term maintenance. — [Style guide goals](https://google.github.io/styleguide/tsguide.html#style-guide-goals).

The source takes precedence over the house style for this task, subject to existing project tooling.

License: [CC-BY-3.0](../LICENSE).

Credit: Google TS/JS Style Guide (formerly the Google TypeScript Style Guide), Google, CC-BY-3.0, https://google.github.io/styleguide/tsguide.html. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.
