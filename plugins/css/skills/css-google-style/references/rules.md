# Google CSS style rules

Google HTML/CSS Style Guide, commit `577f395c` (2026-10-23). Includes the shared General rules and the CSS sections; examples omitted. Each rule links to its original section. Optional choices remain optional.


## Quick rules

- Apply this guide to authored HTML and CSS, including Sass and GSS; build output may be compiled, minified, or obfuscated without sacrificing overall code quality. — [Background](https://google.github.io/styleguide/htmlcssguide.html#Background).
- Before changing a file, inspect nearby code and maintain its established conventions so additions fit their surroundings. — [Parting Words](https://google.github.io/styleguide/htmlcssguide.html#Parting_Words).


## Tooling

- Check CSS with a validator to expose invalid styling and declarations that cannot take effect. — [CSS Validity](https://google.github.io/styleguide/htmlcssguide.html#CSS_Validity).


## Naming

- Favor class names that describe an element's function; use generic helper names when the element has no distinct purpose to name. — [Class Naming](https://google.github.io/styleguide/htmlcssguide.html#ID_and_Class_Naming).
- Reject class names that obscure their meaning or describe only the element's current visual treatment. — [Class Naming](https://google.github.io/styleguide/htmlcssguide.html#ID_and_Class_Naming).
- Make class names as concise as their meaning allows. — [Class Name Style](https://google.github.io/styleguide/htmlcssguide.html#ID_and_Class_Name_Style).
- Join the words or abbreviations in a class name with hyphens. — [Class Name Delimiters](https://google.github.io/styleguide/htmlcssguide.html#ID_and_Class_Name_Delimiters).
- For large applications or styles embedded in other sites, optionally namespace classes with a short, distinctive application prefix followed by a hyphen. — [Prefixes](https://google.github.io/styleguide/htmlcssguide.html#Prefixes).


## Files and layout

- Increase indentation by two spaces for each nesting level. — [Indentation](https://google.github.io/styleguide/htmlcssguide.html#Indentation).
- Use spaces alone for indentation; exclude tabs and mixed indentation. — [Indentation](https://google.github.io/styleguide/htmlcssguide.html#Indentation).
- Lowercase CSS selectors, properties, and non-string values; preserve string casing. — [Capitalization](https://google.github.io/styleguide/htmlcssguide.html#Capitalization).
- Strip spaces and other whitespace from line ends. — [Trailing Whitespace](https://google.github.io/styleguide/htmlcssguide.html#Trailing_Whitespace).
- Save source files as UTF-8 with no leading byte-order mark. — [Encoding](https://google.github.io/styleguide/htmlcssguide.html#Encoding).
- Leave stylesheet encoding undeclared when its assumed UTF-8 encoding suffices. — [Encoding](https://google.github.io/styleguide/htmlcssguide.html#Encoding).
- Maintain a consistent CSS declaration order; alphabetical sorting is an optional convention when tooling does not supply an enforced order. — [Declaration Order](https://google.github.io/styleguide/htmlcssguide.html#Declaration_Order).
- Sort CSS properties by their unprefixed names, keeping each property's vendor variants together and ordering those prefixes alphabetically. — [Declaration Order](https://google.github.io/styleguide/htmlcssguide.html#Declaration_Order).
- Indent the contents of CSS blocks, including declarations and nested rules, to expose nesting. — [Block Content Indentation](https://google.github.io/styleguide/htmlcssguide.html#Block_Content_Indentation).
- Terminate all CSS declarations with semicolons, including the last declaration in a block. — [Declaration Stops](https://google.github.io/styleguide/htmlcssguide.html#Declaration_Stops).
- Attach the colon directly to the CSS property name, then insert exactly one space before its value. — [Property Name Stops](https://google.github.io/styleguide/htmlcssguide.html#Property_Name_Stops).
- Keep the opening CSS brace beside the last selector, separated from it by one space. — [Declaration Block Separation](https://google.github.io/styleguide/htmlcssguide.html#Declaration_Block_Separation).
- Start every CSS selector and every declaration on a separate line. — [Selector and Declaration Separation](https://google.github.io/styleguide/htmlcssguide.html#Selector_and_Declaration_Separation).
- Leave one empty line between adjacent CSS rules. — [Rule Separation](https://google.github.io/styleguide/htmlcssguide.html#Rule_Separation).


## Types and data

- Write CSS zero values without units whenever the grammar allows it. — [0 and Units](https://google.github.io/styleguide/htmlcssguide.html#0_and_Units).
- Include a zero before the decimal point in CSS fractions whose magnitude is below one. — [Leading 0s](https://google.github.io/styleguide/htmlcssguide.html#Leading_0s).
- Use the three-digit hexadecimal color form when it represents exactly the intended color. — [Hexadecimal Notation](https://google.github.io/styleguide/htmlcssguide.html#Hexadecimal_Notation).
- Choose single quotation marks for CSS string values and quoted values in attribute selectors. — [CSS Quotation Marks](https://google.github.io/styleguide/htmlcssguide.html#CSS_Quotation_Marks).
- Write the URI inside CSS `url()` without enclosing quotation marks. — [CSS Quotation Marks](https://google.github.io/styleguide/htmlcssguide.html#CSS_Quotation_Marks).
- If a stylesheet needs `@charset`, enclose its encoding string in double quotation marks as the syntax requires. — [CSS Quotation Marks](https://google.github.io/styleguide/htmlcssguide.html#CSS_Quotation_Marks).


## Comments and docs

- Add explanatory comments where useful to describe the code's coverage, intent, or rationale; exhaustive commenting is optional. — [Comments](https://google.github.io/styleguide/htmlcssguide.html#Comments).
- Identify unfinished work with `TODO`, then a colon and the requested action. — [Action Items](https://google.github.io/styleguide/htmlcssguide.html#Action_Items).
- Optionally label stylesheet sections with grouping comments and place line breaks between sections. — [Section Comments](https://google.github.io/styleguide/htmlcssguide.html#Section_Comments).


## Performance

- Avoid adding an element name to a class selector unless that qualification is necessary. — [Type Selectors](https://google.github.io/styleguide/htmlcssguide.html#Type_Selectors).
- Remove ancestor selectors that are not needed to identify the intended elements. — [Type Selectors](https://google.github.io/styleguide/htmlcssguide.html#Type_Selectors).
- Target classes in stylesheets instead of IDs. — [ID Selectors](https://google.github.io/styleguide/htmlcssguide.html#ID_Selectors).
- Favor CSS shorthand whenever feasible, even if only one constituent value is supplied explicitly. — [Shorthand Properties](https://google.github.io/styleguide/htmlcssguide.html#Shorthand_Properties).


## Security

- Give embedded media, stylesheet, and script URLs an explicit HTTPS scheme whenever the resource is available through HTTPS. — [Protocol](https://google.github.io/styleguide/htmlcssguide.html#Protocol).


## Language-specific pitfalls

- Keep CSS valid, allowing departures for validator bugs or indispensable proprietary syntax. — [CSS Validity](https://google.github.io/styleguide/htmlcssguide.html#CSS_Validity).
- Avoid `!important`; resolve necessary overrides through selector specificity instead. — [Important Declarations](https://google.github.io/styleguide/htmlcssguide.html#Important_Declarations).
- Try other solutions before relying on browser detection or CSS hacks; reserve both for last-resort workarounds. — [Hacks](https://google.github.io/styleguide/htmlcssguide.html#Hacks).

## Worked examples

Read [original worked examples and their source tags](examples.md) for small applications of this guide.
