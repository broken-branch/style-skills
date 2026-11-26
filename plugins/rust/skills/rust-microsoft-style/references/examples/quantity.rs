// [MS-RUST] Opaque errors, captured backtraces and causes: MS:054 through MS:062.
//! Parse quantities while retaining inspectable error context.

use std::backtrace::Backtrace;
use std::error::Error;
use std::fmt;
use std::num::ParseIntError;

/// A quantity failed to parse as an unsigned 16-bit integer.
#[derive(Debug)]
pub struct QuantityError {
    source: ParseIntError,
    backtrace: Backtrace,
}

impl QuantityError {
    /// Borrows the trace captured when the failure entered this API.
    #[must_use]
    pub fn backtrace(&self) -> &Backtrace {
        &self.backtrace
    }

    /// Reports whether the input lacked any digits.
    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.source.kind() == &std::num::IntErrorKind::Empty
    }
}

impl From<ParseIntError> for QuantityError {
    fn from(source: ParseIntError) -> Self {
        Self {
            source,
            backtrace: Backtrace::capture(),
        }
    }
}

impl fmt::Display for QuantityError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "invalid quantity: {}", self.source)
    }
}

impl Error for QuantityError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(&self.source)
    }
}

/// Reads a decimal quantity without trimming the input.
///
/// # Errors
/// Returns an error for empty, malformed or out-of-range input.
///
/// ```
/// assert_eq!(quantity::parse_quantity("512")?, 512);
/// # Ok::<(), quantity::QuantityError>(())
/// ```
pub fn parse_quantity(text: &str) -> Result<u16, QuantityError> {
    Ok(text.parse()?)
}
