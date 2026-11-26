// Go review rules: context propagation [code-review-comments:5],
// synchronous results [code-review-comments:85], ordinary error returns
// [code-review-comments:23].

package catalog

import (
	"context"
	"fmt"
)

func ExampleCatalog_Find() {
	c := New([]string{"cedar", "elm", "cherry"})
	names, err := c.Find(context.Background(), "c")
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(names)
	// Output: [cedar cherry]
}
