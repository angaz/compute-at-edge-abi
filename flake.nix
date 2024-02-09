{
  description = "Description for the project";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    devshell.url = "github:numtide/devshell";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.devshell.flakeModule
      ];

      systems = [
        "aarch64-darwin"
        "aarch64-linux"
        "x86_64-darwin"
        "x86_64-linux"
      ];

      perSystem = { config, self', inputs', pkgs, system, ... }: {
        _module.args.pkgs = import inputs.nixpkgs {
          inherit system;
          overlays = [
            (final: prev: {
              witx-codegen = prev.rustPlatform.buildRustPackage rec {
                pname = "witx-codegen";
                version = "0.11.3";

                src = prev.fetchFromGitHub {
                  owner = "jedisct1";
                  repo = pname;
                  rev = version;
                  hash = "sha256-/mCqqGWthugDjLXXpQZkWlMxFeJDBNWS7ACbyh7Z8Bg=";
                };

                cargoHash = "";
              };
            })
          ];
        };

        devshells.default = {
          packages = with pkgs; [
            # witx-codegen
            (python3.withPackages (p: [
              p.python-lsp-ruff
            ]))
            cargo
            gcc
            rustc
          ];
        };
      };
    };
}
