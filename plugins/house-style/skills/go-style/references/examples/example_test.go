// House rules: runnable documentation with deterministic output [GOOGLE-GO];
// context lifetime and cancellation [GO-CONTEXT]; explicit error handling [UBER-GO].
package limits

import (
	"context"
	"fmt"
)

func ExampleLoad() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	source := lookupFunc(func(ctx context.Context, _ string) (string, error) {
		if err := ctx.Err(); err != nil {
			return "", err
		}
		return "24", nil
	})
	limit, err := Load(ctx, source, "batch")
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(limit)
	// Output: 24
}
