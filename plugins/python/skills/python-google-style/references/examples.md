# Original worked examples

Source tag: `[GOOGLE-PYTHON]` — Google Python Style Guide.

Both modules use descriptive function summaries. count_words consumes an iterable once. on_message retains its callback signature while explicitly deleting unused metadata; its log arguments remain separate from the format string. The direct collections.abc symbol import is the source's typing exception.

## Files

- [Module imports and typed documentation](examples/word_counts.py)
- [Unused callback input and lazy logging](examples/events.py)

## Source sections

- [Imports](https://google.github.io/styleguide/pyguide.html#imports)
- [Lint](https://google.github.io/styleguide/pyguide.html#lint)
- [Functions and methods](https://google.github.io/styleguide/pyguide.html#function-docs)
- [Logging](https://google.github.io/styleguide/pyguide.html#logging)
