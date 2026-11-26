// Google rules: same-package examples [google-go-style:303] [google-go-style:305],
// handling each error [google-go-style:138].

package delay

import "fmt"

func ExampleParseDelay() {
	// A caller in another package would write delay.ParseDelay("750ms").
	d, err := ParseDelay("750ms")
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(d)
	// Output: 750ms
}
