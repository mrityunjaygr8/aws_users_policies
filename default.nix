{ pkgs ? import <nixpkgs> {} }:
let
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix";
    ref = "refs/tags/3.5.0";
  }) {
      python = "python310";
      pypiDataRev =  "fa942bb2bc65ab8a24730c2dacfe60ab03ddf960";
      pypiDataSha256 = "sha256-hK5hzeEkwRk6mpNQFbLjwByp8C7EiwGWxpW13V5XP0Q=";
      pkgs = import <nixpkgs> {};
    };
    deps = mach-nix.mkPython {
      requirements = ''
        boto3
      '';
      # requirements = builtins.readFile ./new_requirements.txt;
      providers = {
        tomli = "nixpkgs";
      };
    };
in pkgs.mkShell {
  # buildInputs is for dependencies you'd need "at run time",
  # were you to to use nix-build not nix-shell and build whatever you were working on
  buildInputs = [
    deps
  ];
}

