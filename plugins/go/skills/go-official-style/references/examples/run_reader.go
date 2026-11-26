// Effective Go rules: interface-only implementation [effective-go:75]
// [effective-go:76], conventional methods [effective-go:71].

// Package runreader supplies finite streams of a repeated byte.
package runreader

import (
	"errors"
	"io"
)

type run struct {
	value     byte
	remaining int
}

// New returns a reader that produces count copies of value.
// A negative count is an error. The implementation intentionally exposes only
// Read; it has no resource to close and no additional methods to discover.
func New(value byte, count int) (io.Reader, error) {
	if count < 0 {
		return nil, errors.New("runreader: negative count")
	}
	return &run{value: value, remaining: count}, nil
}

func (r *run) Read(p []byte) (int, error) {
	if len(p) == 0 {
		return 0, nil
	}
	if r.remaining == 0 {
		return 0, io.EOF
	}
	n := len(p)
	if n > r.remaining {
		n = r.remaining
	}
	for i := 0; i < n; i++ {
		p[i] = r.value
	}
	r.remaining -= n
	return n, nil
}
