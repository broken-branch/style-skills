// [EFFECTIVE-RUST-BOOK] Item 11: Drop and scope-bound rollback.
// Original example; see the source pointer in ../sources.md.
//! Roll back uncommitted byte appends when a guard leaves scope.
//!
//! ```
//! use append_guard::AppendGuard;
//! let mut bytes = vec![1];
//! {
//!     let mut edit = AppendGuard::new(&mut bytes);
//!     edit.append(&[2, 3]);
//! }
//! assert_eq!(bytes, [1]);
//! let mut edit = AppendGuard::new(&mut bytes);
//! edit.append(&[4]);
//! edit.commit();
//! assert_eq!(bytes, [1, 4]);
//! ```

/// An append-only edit that rolls back on normal drop unless committed.
/// Leaking the guard skips rollback; no memory-safety invariant depends on it.
#[derive(Debug)]
pub struct AppendGuard<'a> {
    bytes: &'a mut Vec<u8>,
    original_len: usize,
    committed: bool,
}

impl<'a> AppendGuard<'a> {
    /// Starts an edit while exclusively borrowing the destination.
    pub fn new(bytes: &'a mut Vec<u8>) -> Self {
        let original_len = bytes.len();
        Self {
            bytes,
            original_len,
            committed: false,
        }
    }

    /// Appends bytes to the pending edit.
    pub fn append(&mut self, suffix: &[u8]) {
        self.bytes.extend_from_slice(suffix);
    }

    /// Retains appended bytes and releases the exclusive borrow.
    pub fn commit(mut self) {
        self.committed = true;
    }
}

impl Drop for AppendGuard<'_> {
    fn drop(&mut self) {
        if !self.committed {
            self.bytes.truncate(self.original_len);
        }
    }
}
