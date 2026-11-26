// House rules: borrowed string views and API documentation [RUST-API];
// Unicode scalar boundaries instead of arbitrary byte offsets [CLIPPY].
//! Return a prefix without allocating or splitting a UTF-8 scalar value.

/// Borrows at most `max_chars` Unicode scalar values from `text`.
/// This counts scalar values, not grapheme clusters or display columns.
///
/// ```
/// assert_eq!(unicode_prefix::prefix("aé中", 2), "aé");
/// ```
#[must_use]
pub fn prefix(text: &str, max_chars: usize) -> &str {
    match text.char_indices().nth(max_chars) {
        // char_indices supplies an in-bounds UTF-8 boundary.
        Some((end, _)) => &text[..end],
        None => text,
    }
}

#[cfg(test)]
mod tests {
    use super::prefix;

    #[test]
    fn respects_empty_and_multibyte_boundaries() {
        for (text, count, expected) in [
            ("", 3, ""),
            ("aé中", 0, ""),
            ("aé中", 2, "aé"),
            ("aé中", 3, "aé中"),
            ("aé中", usize::MAX, "aé中"),
            ("e\u{301}", 1, "e"),
        ] {
            assert_eq!(
                prefix(text, count),
                expected,
                "text={text:?}, count={count}"
            );
        }
    }
}
