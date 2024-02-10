# compute-at-edge-abi

Generates the Fatly Compute@Edge ABI for Zig.

## Dependencies

Most of the dependencies are handled by the `flake.nix`, but `witx-codegen`
can't be compiled because it's missing a `Cargo.lock` file, so it has to be
installed via `cargo install witx-codegen`.

## Generate the code

```sh
$ rm *.witx
$ cp ../Viceroy/lib/compute-at-edge-abi/*.witx .
$ ./generate.sh
```
