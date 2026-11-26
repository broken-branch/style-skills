// [RUST-API] C-BUILDER: required inputs and reusable mutable-borrow setters.
// Local rules: API:092, API:093, API:094, API:095.
//! Reuse one card configuration for several independent values.
//!
//! ```
//! use card_builder::CardBuilder;
//! let mut builder = CardBuilder::new("Notice");
//! builder.border('=');
//! let first = builder.build();
//! builder.border('-');
//! assert_eq!(first, "= Notice =");
//! assert_eq!(builder.build(), "- Notice -");
//! ```

/// Reusable configuration for a decorated line of text.
#[derive(Clone, Debug)]
pub struct CardBuilder {
    title: String,
    border: char,
}

impl CardBuilder {
    /// Stores the required title and uses spaces as the initial border.
    pub fn new(title: impl Into<String>) -> Self {
        Self {
            title: title.into(),
            border: ' ',
        }
    }

    /// Chooses the character printed on either side of the title.
    pub fn border(&mut self, border: char) -> &mut Self {
        self.border = border;
        self
    }

    /// Creates a line without consuming or changing this configuration.
    pub fn build(&self) -> String {
        format!("{} {} {}", self.border, self.title, self.border)
    }
}
