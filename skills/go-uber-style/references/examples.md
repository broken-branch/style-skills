# Original worked examples

Source tag: `[UBER-GO]` — Uber Go Style Guide.

These two files form package buffer. Buffer also works without its constructor. WithCapacity controls the initial allocation, not a size limit. The underscore-prefixed private constant follows Uber.

## Files

- [Mutex ownership and copied snapshots](examples/buffer.go)
- [Interface options and private constants](examples/options.go)

## Source sections

- [Interface compliance](https://github.com/uber-go/guide/blob/master/style.md#verify-interface-compliance)
- [Mutexes](https://github.com/uber-go/guide/blob/master/style.md#zero-value-mutexes-are-valid)
- [Slice ownership](https://github.com/uber-go/guide/blob/master/style.md#copy-slices-and-maps-at-boundaries)
- [Functional options](https://github.com/uber-go/guide/blob/master/style.md#functional-options)
