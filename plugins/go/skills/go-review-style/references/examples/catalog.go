// Go review rules: concrete producer results [code-review-comments:50],
// passed contexts [code-review-comments:6] [code-review-comments:8],
// synchronous work [code-review-comments:85] [code-review-comments:86].

// Package catalog provides an immutable in-memory name catalog.
package catalog

import (
	"context"
	"strings"
)

// Catalog owns its name list. Its methods may be called concurrently.
type Catalog struct {
	names []string
}

// New copies names so subsequent caller mutations cannot change the catalog.
func New(names []string) *Catalog {
	return &Catalog{names: append([]string(nil), names...)}
}

// Find returns names beginning with prefix, preserving input order.
// It returns nil when there are no matches, and discards partial results on
// cancellation. It starts no goroutines and retains no context.
func (c *Catalog) Find(ctx context.Context, prefix string) ([]string, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	var matches []string
	for _, name := range c.names {
		if err := ctx.Err(); err != nil {
			return nil, err
		}
		if strings.HasPrefix(name, prefix) {
			matches = append(matches, name)
		}
	}
	return matches, nil
}
