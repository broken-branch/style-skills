// House rules: opaque contextual errors and preserved causes [MS-RUST];
// borrowed inputs, error traits and API docs [RUST-API]; propagation [CLIPPY].
//! Parse an unsigned count while retaining the caller's field name.

use std::error::Error;
use std::fmt;
use std::num::ParseIntError;

/// A count could not be parsed. Inspect the original cause with `Error::source`.
#[derive(Debug)]
pub struct CountError {
    field: &'static str,
    source: ParseIntError,
}

impl CountError {
    /// Returns the field being parsed, without including the supplied value.
    #[must_use]
    pub fn field(&self) -> &'static str {
        self.field
    }
}

impl fmt::Display for CountError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "invalid count for {}", self.field)
    }
}

impl Error for CountError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(&self.source)
    }
}

/// Parses a decimal count without trimming whitespace.
///
/// # Errors
/// Returns a `CountError` containing the field and original `ParseIntError`
/// for invalid input or a value outside the `u32` range.
pub fn parse_count(field: &'static str, input: &str) -> Result<u32, CountError> {
    let count = input
        .parse()
        .map_err(|source| CountError { field, source })?;
    Ok(count)
}

#[cfg(test)]
mod tests {
    use super::parse_count;
    use std::error::Error;
    use std::num::ParseIntError;

    #[test]
    fn parses_counts_and_retains_error_context() {
        assert_eq!(parse_count("items", "0").unwrap(), 0);
        assert_eq!(parse_count("items", "4294967295").unwrap(), u32::MAX);

        for input in ["", "-1", "two", " 2", "4294967296"] {
            let error = parse_count("items", input).unwrap_err();
            assert_eq!(error.field(), "items");
            assert!(error.source().unwrap().is::<ParseIntError>());
        }
    }

    #[test]
    fn error_can_cross_thread_boundaries() {
        fn require_send_sync<T: Send + Sync>() {}
        require_send_sync::<super::CountError>();
    }
}
