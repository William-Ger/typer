{
  description = "Typing practice in your terminal";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;
      in
      {
        packages = {
          default = python.pkgs.buildPythonApplication {
            pname = "typer-cli-tool";
            version = "0.5.2";
            src = ./.;
            format = "pyproject";

            nativeBuildInputs = [ python.pkgs.setuptools ];

            meta = {
              description = "Typing practice in your terminal";
              homepage = "https://github.com/William-Ger/typer";
              license = pkgs.lib.licenses.mit;
              mainProgram = "typer";
            };
          };
        };

        devShells.default = pkgs.mkShell {
          packages = [
            python
            python.pkgs.setuptools
            python.pkgs.pip
          ];
        };
      }
    );
}
