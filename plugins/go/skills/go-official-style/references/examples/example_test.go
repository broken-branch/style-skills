// Effective Go rules: narrow interfaces [effective-go:72], handle errors
// [effective-go:80], ordinary unformatted printing [effective-go:60].

package runreader

import (
	"fmt"
	"io"
)

func ExampleNew() {
	r, err := New('.', 4)
	if err != nil {
		fmt.Println(err)
		return
	}
	data, err := io.ReadAll(r)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(string(data))
	// Output: ....
}
