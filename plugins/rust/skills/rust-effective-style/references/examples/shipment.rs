// [EFFECTIVE-RUST-BOOK] Item 1: data-carrying alternatives.
// Original example; see the source pointer in ../sources.md.
//! Shipment state keeps a tracking number only where it is meaningful.

/// The current phase of a shipment.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum Shipment {
    /// The parcel has not been dispatched.
    Packed,
    /// The parcel is moving under a carrier's tracking number.
    InTransit { tracking_number: String },
    /// Delivery is complete and no tracking lookup is needed.
    Delivered,
}

impl Shipment {
    /// Borrows the tracking number when a shipment is in transit.
    ///
    /// ```
    /// use shipment::Shipment;
    /// assert_eq!(Shipment::Packed.tracking_number(), None);
    /// let parcel = Shipment::InTransit { tracking_number: "PK-42".into() };
    /// assert_eq!(parcel.tracking_number(), Some("PK-42"));
    /// ```
    pub fn tracking_number(&self) -> Option<&str> {
        match self {
            Self::InTransit { tracking_number } => Some(tracking_number),
            Self::Packed | Self::Delivered => None,
        }
    }
}
