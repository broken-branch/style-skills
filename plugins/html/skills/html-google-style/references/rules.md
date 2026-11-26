# Google HTML style rules

Google HTML/CSS Style Guide, commit `577f395c` (2026-10-23). Includes the shared General rules and the HTML sections; examples omitted. Each rule links to its original section. Optional choices remain optional.


## Quick rules

- Apply this guide to authored HTML and CSS, including Sass and GSS; build output may be compiled, minified, or obfuscated without sacrificing overall code quality. — [Background](https://google.github.io/styleguide/htmlcssguide.html#Background).
- Before changing a file, inspect nearby code and maintain its established conventions so additions fit their surroundings. — [Parting Words](https://google.github.io/styleguide/htmlcssguide.html#Parting_Words).


## Tooling

- Check HTML with a markup validator. — [HTML Validity](https://google.github.io/styleguide/htmlcssguide.html#HTML_Validity).
- Adopt a uniform HTML wrapping convention across the project, ideally maintained by automated formatting. — [HTML Line-Wrapping](https://google.github.io/styleguide/htmlcssguide.html#HTML_Line-Wrapping).


## Naming

- Add an HTML `id` only when it is needed. — [`id` Attributes](https://google.github.io/styleguide/htmlcssguide.html#id_Attributes).
- Favor classes as styling hooks and data attributes as scripting hooks. — [`id` Attributes](https://google.github.io/styleguide/htmlcssguide.html#id_Attributes).
- Put a hyphen in every necessary ID so its value cannot be used as a bare JavaScript identifier; it remains accessible as a named property. — [`id` Attributes](https://google.github.io/styleguide/htmlcssguide.html#id_Attributes).


## Files and layout

- Increase indentation by two spaces for each nesting level. — [Indentation](https://google.github.io/styleguide/htmlcssguide.html#Indentation).
- Use spaces alone for indentation; exclude tabs and mixed indentation. — [Indentation](https://google.github.io/styleguide/htmlcssguide.html#Indentation).
- Write HTML names, attributes, and non-text attribute values in lowercase; preserve text and CDATA casing. — [Capitalization](https://google.github.io/styleguide/htmlcssguide.html#Capitalization).
- Strip spaces and other whitespace from line ends. — [Trailing Whitespace](https://google.github.io/styleguide/htmlcssguide.html#Trailing_Whitespace).
- Save source files as UTF-8 with no leading byte-order mark. — [Encoding](https://google.github.io/styleguide/htmlcssguide.html#Encoding).
- Include a UTF-8 charset declaration in the metadata of HTML documents and templates. — [Encoding](https://google.github.io/styleguide/htmlcssguide.html#Encoding).
- Start each HTML document with `<!doctype html>` to obtain no-quirks rendering. — [Document Type](https://google.github.io/styleguide/htmlcssguide.html#Document_Type).
- Keep documents and templates structural, moving presentation into stylesheets and behavior into scripts. — [Separation of Concerns](https://google.github.io/styleguide/htmlcssguide.html#Separation_of_Concerns).
- Begin each block, list, or table element on a fresh line and indent such elements when nested, regardless of their CSS display settings. — [General Formatting](https://google.github.io/styleguide/htmlcssguide.html#General_Formatting).
- When whitespace between list items breaks the intended rendering, the items may share one line; prefer reporting this formatting exception as a lint warning. — [General Formatting](https://google.github.io/styleguide/htmlcssguide.html#General_Formatting).
- Wrap lengthy HTML lines if doing so materially improves readability; Google specifies no fixed column ceiling. — [HTML Line-Wrapping](https://google.github.io/styleguide/htmlcssguide.html#HTML_Line-Wrapping).
- Indent wrapped HTML lines so continued attributes are visually distinct from child elements. — [HTML Line-Wrapping](https://google.github.io/styleguide/htmlcssguide.html#HTML_Line-Wrapping).
- When an HTML attribute value is quoted, surround it with double quotation marks. — [HTML Quotation Marks](https://google.github.io/styleguide/htmlcssguide.html#HTML_Quotation_Marks).


## Types and data

- Write UTF-8 characters directly instead of using HTML character references, except where HTML syntax or invisible/control characters require references. — [Entity References](https://google.github.io/styleguide/htmlcssguide.html#Entity_References).


## Comments and docs

- Add explanatory comments where useful to describe the code's coverage, intent, or rationale; exhaustive commenting is optional. — [Comments](https://google.github.io/styleguide/htmlcssguide.html#Comments).
- Identify unfinished work with `TODO`, then a colon and the requested action. — [Action Items](https://google.github.io/styleguide/htmlcssguide.html#Action_Items).


## Performance

- Reduce the stylesheet and script references in each document or template and keep their interaction with markup small. — [Separation of Concerns](https://google.github.io/styleguide/htmlcssguide.html#Separation_of_Concerns).
- Tag omission is an optional size/readability choice: omit only tags HTML permits omitting, and prefer applying that choice throughout rather than selectively. — [Optional Tags](https://google.github.io/styleguide/htmlcssguide.html#Optional_Tags).


## Security

- Give embedded media, stylesheet, and script URLs an explicit HTTPS scheme whenever the resource is available through HTTPS. — [Protocol](https://google.github.io/styleguide/htmlcssguide.html#Protocol).


## Language-specific pitfalls

- Keep HTML valid unless a file-size performance target cannot otherwise be met. — [HTML Validity](https://google.github.io/styleguide/htmlcssguide.html#HTML_Validity).
- Choose HTML elements whose defined meaning matches the content or interaction being represented. — [Semantics](https://google.github.io/styleguide/htmlcssguide.html#Semantics).
- Provide alternate access to multimedia, using meaningful image alternatives and, where available, captions and transcripts for video and audio. — [Multimedia Fallback](https://google.github.io/styleguide/htmlcssguide.html#Multimedia_Fallback).
- Give an image empty alternative text when describing it would repeat existing information, or when it is purely decorative and cannot readily be implemented in CSS. — [Multimedia Fallback](https://google.github.io/styleguide/htmlcssguide.html#Multimedia_Fallback).
- Drop redundant MIME type attributes from CSS resources and ordinary JavaScript script elements. — [`type` Attributes](https://google.github.io/styleguide/htmlcssguide.html#type_Attributes).
- Preserve the module type on module scripts and declare other types when content differs from the CSS or JavaScript defaults. — [`type` Attributes](https://google.github.io/styleguide/htmlcssguide.html#type_Attributes).

## Worked examples

Read [original worked examples and their source tags](examples.md) for small applications of this guide.
