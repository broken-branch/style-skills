// [EFFECTIVE-RUST-BOOK] Item 4: error enums, nested causes and From.
// Original example; see the source pointer in ../sources.md.
//! Parse a pair of signed grid coordinates without erasing error categories.

use std::error::Error;
use std::fmt;
use std::num::ParseIntError;

/// Why a coordinate pair could not be read.
#[derive(Debug)]
pub enum CoordinateError {
    /// The pair has no colon separator.
    MissingSeparator,
    /// A component is not a valid signed 32-bit integer.
    InvalidInteger(ParseIntError),
}

impl fmt::Display for CoordinateError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::MissingSeparator => formatter.write_str("coordinate separator missing"),
            Self::InvalidInteger(error) => write!(formatter, "invalid coordinate: {}", error),
        }
    }
}

impl Error for CoordinateError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::MissingSeparator => None,
            Self::InvalidInteger(error) => Some(error),
        }
    }
}

impl From<ParseIntError> for CoordinateError {
    fn from(error: ParseIntError) -> Self {
        Self::InvalidInteger(error)
    }
}

/// Parses `horizontal:vertical`, preserving signs and rejecting whitespace.
///
/// # Errors
/// Returns a missing-separator or integer-parsing error.
///
/// ```
/// use coordinate::{parse_coordinate, CoordinateError};
/// assert_eq!(parse_coordinate("-3:8")?, (-3, 8));
/// assert!(matches!(parse_coordinate("3"), Err(CoordinateError::MissingSeparator)));
/// # Ok::<(), CoordinateError>(())
/// ```
pub fn parse_coordinate(text: &str) -> Result<(i32, i32), CoordinateError> {
    let (horizontal, vertical) = text
        .split_once(':')
        .ok_or(CoordinateError::MissingSeparator)?;
    Ok((horizontal.parse()?, vertical.parse()?))
}
