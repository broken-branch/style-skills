// Go review rules: informative failures [code-review-comments:87]
// [code-review-comments:88], nil empty slices [code-review-comments:18].

package catalog

import (
	"context"
	"errors"
	"testing"
)

func TestFindOwnsNames(t *testing.T) {
	names := []string{"elm", "oak"}
	c := New(names)
	names[0] = "ash"
	got, err := c.Find(context.Background(), "el")
	if err != nil {
		t.Fatalf("Find(el) error = %v; want nil", err)
	}
	if len(got) != 1 || got[0] != "elm" {
		t.Errorf("Find(el) = %q; want [elm] after input mutation", got)
	}
}

func TestFindNoMatches(t *testing.T) {
	got, err := New([]string{"elm"}).Find(context.Background(), "z")
	if got != nil || err != nil {
		t.Errorf("Find(z) = %q, %v; want nil, nil", got, err)
	}
}

func TestFindCanceledEmptyCatalog(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	got, err := New(nil).Find(ctx, "")
	if got != nil || !errors.Is(err, context.Canceled) {
		t.Errorf("Find on canceled context = %q, %v; want nil, context.Canceled", got, err)
	}
}
