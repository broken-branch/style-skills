// [GOOGLE-RUST] Constructor names and public enums: GOOGLE:090, GOOGLE:123.
//! A small retry policy with an explicitly named alternative constructor.
//!
//! ```
//! use retry_policy::{Decision, RetryPolicy};
//! let policy = RetryPolicy::new_with_limit(2);
//! assert_eq!(policy.decide(1), Decision::Retry);
//! assert_eq!(policy.decide(2), Decision::Stop);
//! ```

/// The action after a failed attempt.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
#[non_exhaustive]
pub enum Decision {
    /// Attempt the operation again.
    Retry,
    /// Return the failure to the caller.
    Stop,
}

/// Limits the number of retries after the initial attempt.
#[derive(Clone, Copy, Debug, Default)]
pub struct RetryPolicy {
    limit: u32,
}

impl RetryPolicy {
    /// Creates a policy that never retries.
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    /// Creates a policy with a caller-selected retry limit.
    #[must_use]
    pub fn new_with_limit(limit: u32) -> Self {
        Self { limit }
    }

    /// Chooses an action given the number of retries already performed.
    #[must_use]
    pub fn decide(&self, retries: u32) -> Decision {
        if retries < self.limit {
            Decision::Retry
        } else {
            Decision::Stop
        }
    }
}
