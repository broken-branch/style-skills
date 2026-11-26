// Uber rules: interface-based functional options, private global naming,
// and explicit error returns [UBER-GO].
package buffer

import (
	"errors"
	"fmt"
)

const _defaultCapacity = 32

// Option changes a buffer's initial allocation.
type Option interface {
	apply(*options)
}

type options struct {
	capacity int
}

// New creates an empty buffer. Later options override earlier ones.
// Nil options and a negative final capacity produce errors.
func New(opts ...Option) (*Buffer, error) {
	settings := options{capacity: _defaultCapacity}
	for _, opt := range opts {
		if opt == nil {
			return nil, errors.New("buffer option must not be nil")
		}
		opt.apply(&settings)
	}
	if settings.capacity < 0 {
		return nil, fmt.Errorf(
			"buffer capacity must be non-negative: %d", settings.capacity,
		)
	}
	return &Buffer{data: make([]byte, 0, settings.capacity)}, nil
}

// WithCapacity sets an allocation hint, not a limit on future writes.
// A capacity of zero defers allocation until data is written.
func WithCapacity(capacity int) Option {
	return capacityOption(capacity)
}

type capacityOption int

func (c capacityOption) apply(settings *options) {
	settings.capacity = int(c)
}
