// [MS-RUST] Standard ranges and reference inputs: MS:034, MS:036, MS:037.
//! Count measurements using the caller's preferred range boundaries.

use std::ops::RangeBounds;

/// Counts values inside `range`, accepting any byte-slice-compatible input.
///
/// ```
/// use range_count::count_in;
/// assert_eq!(count_in([2, 4, 6], 2..6), 2);
/// assert_eq!(count_in(vec![2, 4, 6], ..=6), 3);
/// assert_eq!(count_in([], ..), 0);
/// ```
#[must_use]
pub fn count_in(values: impl AsRef<[u8]>, range: impl RangeBounds<u8>) -> usize {
    values
        .as_ref()
        .iter()
        .filter(|value| range.contains(value))
        .count()
}
