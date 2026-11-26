// [RUST-API] C-RW-VALUE, C-QUESTION-MARK, C-FAILURE: generic I/O and errors.
// Local rules: API:039, API:040, API:052, API:054.
//! Write a record to either an owned writer or a mutable borrow.

use std::io::{self, Write};

/// Writes the exact payload followed by a newline; does not flush the writer.
///
/// A mutable reference is also a writer, so callers can retain their buffer.
///
/// # Errors
/// Returns the writer's error. A failed write can leave partial output.
///
/// ```
/// let mut bytes = Vec::new();
/// write_record::write_record(&mut bytes, b"ready")?;
/// write_record::write_record(std::io::sink(), b"discarded")?;
/// assert_eq!(bytes, b"ready\n");
/// # Ok::<(), std::io::Error>(())
/// ```
pub fn write_record<W: Write>(mut writer: W, payload: &[u8]) -> io::Result<()> {
    writer.write_all(payload)?;
    writer.write_all(b"\n")
}
