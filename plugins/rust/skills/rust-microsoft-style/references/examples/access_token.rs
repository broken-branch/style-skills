// [MS-RUST] Sensitive Debug and Display redaction: MS:007, MS:008, MS:010.
//! A token whose diagnostic forms never include its bytes.

use std::fmt;

/// Holds a token with redacted formatting; storage is not encrypted or zeroized.
pub struct AccessToken {
    bytes: Vec<u8>,
}

impl AccessToken {
    /// Takes ownership of token bytes.
    #[must_use]
    pub fn new(bytes: Vec<u8>) -> Self {
        Self { bytes }
    }

    /// Explicitly borrows bytes for an authentication boundary.
    #[must_use]
    pub fn as_bytes(&self) -> &[u8] {
        &self.bytes
    }
}

impl fmt::Debug for AccessToken {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str("AccessToken(<redacted>)")
    }
}

impl fmt::Display for AccessToken {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str("<redacted>")
    }
}
