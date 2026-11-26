// House rules: named table tests and explicit checks [GOOGLE-GO] [GO-TEST];
// wrapped-error identity [GO-REVIEW]; context propagation [GO-CONTEXT].
package limits

import (
	"context"
	"errors"
	"strconv"
	"testing"
)

type lookupFunc func(context.Context, string) (string, error)

func (f lookupFunc) Lookup(ctx context.Context, key string) (string, error) {
	return f(ctx, key)
}

func TestLoad(t *testing.T) {
	errUnavailable := errors.New("source unavailable")
	tests := []struct {
		name      string
		text      string
		sourceErr error
		cancel    bool
		want      uint16
		wantErr   error
	}{
		{name: "zero", text: "0"},
		{name: "ordinary", text: "24", want: 24},
		{name: "upper bound", text: "65535", want: 65535},
		{name: "empty", wantErr: strconv.ErrSyntax},
		{name: "negative", text: "-1", wantErr: strconv.ErrSyntax},
		{name: "overflow", text: "65536", wantErr: strconv.ErrRange},
		{name: "source failure", sourceErr: errUnavailable, wantErr: errUnavailable},
		{name: "canceled", cancel: true, wantErr: context.Canceled},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			ctx, cancel := context.WithCancel(t.Context())
			defer cancel()
			if tt.cancel {
				cancel()
			}
			called := false
			source := lookupFunc(func(gotCtx context.Context, key string) (string, error) {
				called = true
				if gotCtx != ctx || key != "batch" {
					t.Errorf("Lookup received context %v and key %q; want original context and batch", gotCtx, key)
				}
				return tt.text, tt.sourceErr
			})
			got, err := Load(ctx, source, "batch")
			if !errors.Is(err, tt.wantErr) {
				t.Fatalf("Load(%q) error = %v, want identity %v", tt.text, err, tt.wantErr)
			}
			if got != tt.want {
				t.Errorf("Load(%q) = %d, want %d", tt.text, got, tt.want)
			}
			if called == tt.cancel {
				t.Errorf("Lookup called = %t, want %t", called, !tt.cancel)
			}
			if errors.Is(err, strconv.ErrSyntax) || errors.Is(err, strconv.ErrRange) {
				var parseErr *strconv.NumError
				if !errors.As(err, &parseErr) {
					t.Errorf("Load(%q) error = %v, want *strconv.NumError cause", tt.text, err)
				}
			}
		})
	}
}
