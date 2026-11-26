// [GOOGLE-RUST] Scoped enum globs and local trait imports: GOOGLE:021, GOOGLE:026.
//! Format directions with imports confined to their consuming methods.

/// A permanently fixed pair of directions along a line.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Direction {
    /// Toward the line's beginning.
    Backward,
    /// Toward the line's end.
    Forward,
}

impl Direction {
    /// Returns the opposite direction.
    #[must_use]
    pub fn reversed(self) -> Self {
        use Direction::*;
        match self {
            Backward => Forward,
            Forward => Backward,
        }
    }

    /// Writes a direction and a step count into a caller-provided string.
    ///
    /// # Errors
    /// Propagates formatting errors; the standard string writer cannot fail.
    ///
    /// ```
    /// use direction::Direction;
    /// let mut line = String::new();
    /// Direction::Forward.reversed().write_steps(&mut line, 3)?;
    /// assert_eq!(line, "Backward: 3");
    /// # Ok::<(), std::fmt::Error>(())
    /// ```
    pub fn write_steps(self, output: &mut String, steps: u32) -> std::fmt::Result {
        use std::fmt::Write;
        write!(output, "{self:?}: {steps}")
    }
}
