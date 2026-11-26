// [GOOGLE-RUST] Ownership-revealing accessors: GOOGLE:112 through GOOGLE:114.
//! A label slot whose methods distinguish borrowing, replacing and taking.
//!
//! ```
//! use label_slot::LabelSlot;
//! let mut slot = LabelSlot::default();
//! assert_eq!(slot.replace_label("first".into()), None);
//! assert_eq!(slot.label(), Some("first"));
//! assert_eq!(slot.take_label().as_deref(), Some("first"));
//! assert_eq!(slot.label(), None);
//! ```

/// Holds a label until a consumer takes ownership.
#[derive(Clone, Debug, Default)]
pub struct LabelSlot {
    label: Option<String>,
}

impl LabelSlot {
    /// Borrows the current label, if one exists.
    #[must_use]
    pub fn label(&self) -> Option<&str> {
        self.label.as_deref()
    }

    /// Installs a label and returns ownership of the previous one.
    pub fn replace_label(&mut self, label: String) -> Option<String> {
        self.label.replace(label)
    }

    /// Removes the current label and transfers ownership to the caller.
    pub fn take_label(&mut self) -> Option<String> {
        self.label.take()
    }
}
