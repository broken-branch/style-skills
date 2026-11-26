// Uber rules: interface compliance, a named zero-value mutex, deferred unlocks,
// and copies at slice ownership boundaries [UBER-GO].

// Package buffer provides a synchronized byte buffer with snapshot reads.
package buffer

import (
	"io"
	"sync"
)

// Buffer owns its bytes. Its zero value is ready to use.
// A Buffer must not be copied after first use.
type Buffer struct {
	mu   sync.Mutex
	data []byte
}

var _ io.Writer = (*Buffer)(nil)

// Write appends a copy of data and always returns len(data), nil.
func (b *Buffer) Write(data []byte) (int, error) {
	b.mu.Lock()
	defer b.mu.Unlock()

	b.data = append(b.data, data...)
	return len(data), nil
}

// Snapshot returns an independent copy of the buffer, or nil when empty.
func (b *Buffer) Snapshot() []byte {
	b.mu.Lock()
	defer b.mu.Unlock()

	if len(b.data) == 0 {
		return nil
	}
	data := make([]byte, len(b.data))
	copy(data, b.data)
	return data
}
