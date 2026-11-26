// [RUST-STYLE] Wrapped where predicates and chains: RSG:072, RSG:073, RSG:159.
//! Merge two count sequences into a sorted histogram.

use std::collections::BTreeMap;

/// Adds counts by key across two iterators, saturating at the `u64` maximum.
///
/// ```
/// let totals = merge_counts::merge_counts([("oak", 2)], [("oak", 3), ("elm", 1)]);
/// assert_eq!(totals.get("oak"), Some(&5));
/// assert_eq!(totals.get("elm"), Some(&1));
/// ```
pub fn merge_counts<K, I, J>(first: I, second: J) -> BTreeMap<K, u64>
where
    K: Ord,
    I: IntoIterator<Item = (K, u32)>,
    J: IntoIterator<Item = (K, u32)>,
{
    let mut counts = BTreeMap::new();
    for (key, count) in first.into_iter().chain(second) {
        counts
            .entry(key)
            .and_modify(|total: &mut u64| *total = total.saturating_add(u64::from(count)))
            .or_insert(u64::from(count));
    }
    counts
}
