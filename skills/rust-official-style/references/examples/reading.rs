// [RUST-STYLE] Enum layout and block match arms: RSG:042, RSG:171, RSG:175.
//! Classify readings with expression-valued and statement-valued match arms.

/// A recorded measurement or a reason it is unavailable.
#[derive(Clone, Copy, Debug)]
pub enum Reading {
    /// A signed sample.
    Value(i32),
    /// No sample arrived.
    Missing,
    /// The sensor reported a fault.
    Fault,
}

/// Formats a reading, appending a diagnostic when a sensor fault occurs.
///
/// ```
/// let mut diagnostics = Vec::new();
/// let label = reading::describe(reading::Reading::Fault, &mut diagnostics);
/// assert_eq!(label, "unavailable");
/// assert_eq!(diagnostics, ["sensor fault"]);
/// ```
pub fn describe(reading: Reading, diagnostics: &mut Vec<&'static str>) -> String {
    match reading {
        Reading::Value(value) => value.to_string(),
        Reading::Missing => "missing".to_owned(),
        Reading::Fault => {
            diagnostics.push("sensor fault");
            "unavailable".to_owned()
        }
    }
}
