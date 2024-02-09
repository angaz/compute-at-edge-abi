#!/usr/bin/env bash

rm -rf witx

python3 transform.py compute-at-edge.witx

~/.cargo/bin/witx-codegen --output-type zig witx/typenames.witx witx/fastly_*.witx > wasm.zig
