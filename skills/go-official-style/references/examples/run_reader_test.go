// Effective Go rules: check errors [effective-go:80], grouped imports
// and gofmt [effective-go:3], separate results and status [effective-go:37].

package runreader

import (
	"io"
	"testing"
)

func TestReadInChunks(t *testing.T) {
	r, err := New('x', 3)
	if err != nil {
		t.Fatal(err)
	}
	var buf [2]byte
	for _, want := range []string{"xx", "x"} {
		n, err := r.Read(buf[:])
		if err != nil {
			t.Fatalf("Read = %d, %v; want %d, nil", n, err, len(want))
		}
		if got := string(buf[:n]); got != want {
			t.Errorf("Read bytes = %q; want %q", got, want)
		}
	}
	if n, err := r.Read(nil); n != 0 || err != nil {
		t.Errorf("Read(nil) = %d, %v; want 0, nil", n, err)
	}
	if n, err := r.Read(buf[:]); n != 0 || err != io.EOF {
		t.Errorf("Read after exhaustion = %d, %v; want 0, EOF", n, err)
	}
}

func TestNewNegative(t *testing.T) {
	if r, err := New('x', -1); r != nil || err == nil {
		t.Errorf("New('x', -1) = %v, %v; want nil, error", r, err)
	}
}
