// House rules: validated newtypes and lawful common traits [RUST-API];
// fallible constructor naming [GOOGLE-RUST]; explicit Result failures [MS-RUST].
//! A nonzero batch size that cannot be constructed in an invalid state.

use std::num::NonZeroU16;
use std::num::TryFromIntError;

/// The number of items processed in one batch, from 1 through 65535.
#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[must_use]
pub struct BatchSize(NonZeroU16);

impl BatchSize {
    /// Validates the requested batch size.
    ///
    /// # Errors
    /// Returns `TryFromIntError` when `value` is zero.
    pub fn try_new(value: u16) -> Result<Self, TryFromIntError> {
        Ok(Self(NonZeroU16::try_from(value)?))
    }

    /// Returns the validated number of items.
    #[must_use]
    pub fn items(self) -> u16 {
        self.0.get()
    }
}

#[cfg(test)]
mod tests {
    use super::BatchSize;

    #[test]
    fn rejects_zero_and_accepts_both_bounds() {
        assert!(BatchSize::try_new(0).is_err());
        for items in [1, 16, u16::MAX] {
            assert_eq!(BatchSize::try_new(items).unwrap().items(), items);
        }
    }
}
