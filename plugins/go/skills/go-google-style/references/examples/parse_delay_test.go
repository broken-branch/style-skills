// Google rules: table tests [google-go-style:294], readable subtest names
// [google-go-style:291], inline checks [google-go-style:452] [google-go-style:480].

package delay

import (
	"testing"
	"time"
)

func TestParseDelay(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		want    time.Duration
		wantErr bool
	}{
		{name: "seconds", input: "3s", want: 3 * time.Second},
		{name: "fraction", input: "1.5ms", want: 1500 * time.Microsecond},
		{name: "zero", input: "0"},
		{name: "negative", input: "-2s", wantErr: true},
		{name: "missing_unit", input: "3", wantErr: true},
		{name: "empty", input: "", wantErr: true},
		{name: "control_character", input: "\n", wantErr: true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ParseDelay(tt.input)
			if (err != nil) != tt.wantErr {
				t.Fatalf("ParseDelay(%q) = %v, %v; want error: %t", tt.input, got, err, tt.wantErr)
			}
			if tt.wantErr {
				return
			}
			if got != tt.want {
				t.Errorf("ParseDelay(%q) = %v; want %v", tt.input, got, tt.want)
			}
		})
	}
}
