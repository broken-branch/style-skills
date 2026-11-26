// [RUST-API] C-CONV, C-CTOR, C-COMMON-TRAITS: views, ownership, with_ naming.
// Local rules: API:009, API:010, API:022, API:077.
//! A byte buffer with explicit borrowing and ownership transfer.
//!
//! ```
//! use byte_buffer::ByteBuffer;
//! let mut buffer = ByteBuffer::with_capacity(8);
//! buffer.push(42);
//! assert_eq!(buffer.as_slice(), &[42]);
//! assert_eq!(buffer.into_inner(), vec![42]);
//! ```

/// An owned sequence of bytes.
#[derive(Clone, Debug, Default, Eq, Hash, PartialEq)]
pub struct ByteBuffer(Vec<u8>);

impl ByteBuffer {
    /// Creates an empty buffer.
    pub fn new() -> Self {
        Self::default()
    }

    /// Reserves room for at least `capacity` bytes.
    pub fn with_capacity(capacity: usize) -> Self {
        Self(Vec::with_capacity(capacity))
    }

    /// Appends one byte.
    pub fn push(&mut self, byte: u8) {
        self.0.push(byte);
    }

    /// Borrows the stored bytes without copying them.
    pub fn as_slice(&self) -> &[u8] {
        &self.0
    }

    /// Transfers the allocation to the caller.
    pub fn into_inner(self) -> Vec<u8> {
        self.0
    }
}

impl From<Vec<u8>> for ByteBuffer {
    fn from(bytes: Vec<u8>) -> Self {
        Self(bytes)
    }
}

impl AsRef<[u8]> for ByteBuffer {
    fn as_ref(&self) -> &[u8] {
        self.as_slice()
    }
}
