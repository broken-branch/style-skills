// Google rules: quoted diagnostics [google-go-style:222] [google-go-style:223],
// error flow [google-go-style:143], explicit returns [google-go-style:108].

// Package delay parses nonnegative scheduling delays.
package delay

import (
	"fmt"
	"time"
)

// ParseDelay accepts Go duration syntax, including zero, and rejects negatives.
func ParseDelay(text string) (time.Duration, error) {
	d, err := time.ParseDuration(text)
	if err != nil {
		return 0, fmt.Errorf("parse delay %q: %w", text, err)
	}
	if d < 0 {
		return 0, fmt.Errorf("delay %q must be nonnegative", text)
	}
	return d, nil
}
