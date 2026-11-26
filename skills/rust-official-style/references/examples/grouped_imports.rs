// [RUST-STYLE] Nested imports and version order: RSG:035, RSG:087, RSG:092.
//! Render sorted, deduplicated labels with a nested import group.

use std::{
    collections::{BTreeMap, BTreeSet},
    fmt::Write,
};

/// Groups labels by their first Unicode scalar and sorts each group.
///
/// # Errors
/// Propagates a formatting error; string formatting cannot fail here.
///
/// ```
/// let output = grouped_imports::group_labels(&["beta", "ant", "ant", ""])?;
/// assert_eq!(output, "a: ant\nb: beta\n");
/// # Ok::<(), std::fmt::Error>(())
/// ```
pub fn group_labels(labels: &[&str]) -> Result<String, std::fmt::Error> {
    let mut groups: BTreeMap<char, BTreeSet<&str>> = BTreeMap::new();
    for label in labels {
        if let Some(initial) = label.chars().next() {
            groups.entry(initial).or_default().insert(label);
        }
    }
    let mut output = String::new();
    for (initial, labels) in groups {
        for label in labels {
            writeln!(output, "{initial}: {label}")?;
        }
    }
    Ok(output)
}
