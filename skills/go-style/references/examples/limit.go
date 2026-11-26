// House rules: context-first requests [GO-CONTEXT]; consumer interfaces and
// wrapped errors [GO-REVIEW] [UBER-GO]; exported contracts [GOOGLE-GO].

// Package limits loads bounded numeric settings from a caller-owned source.
package limits

import (
	"context"
	"fmt"
	"strconv"
)

// TextSource supplies a setting and must honor the caller's cancellation.
type TextSource interface {
	// Lookup returns the setting for key, or an error if the lookup fails.
	Lookup(ctx context.Context, key string) (string, error)
}

// Load reads key and parses an unsigned 16-bit decimal limit.
// It passes ctx unchanged to source and starts no goroutines.
// Errors wrap ctx.Err(), the source's error, or *strconv.NumError, preserving
// their identities for errors.Is and errors.As. Zero is a valid limit.
func Load(ctx context.Context, source TextSource, key string) (uint16, error) {
	if err := ctx.Err(); err != nil {
		return 0, fmt.Errorf("load limit %q: %w", key, err)
	}
	text, err := source.Lookup(ctx, key)
	if err != nil {
		return 0, fmt.Errorf("lookup limit %q: %w", key, err)
	}
	value, err := strconv.ParseUint(text, 10, 16)
	if err != nil {
		return 0, fmt.Errorf("parse limit %q: %w", key, err)
	}
	return uint16(value), nil
}
