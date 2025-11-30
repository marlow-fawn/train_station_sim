{ pkgs, ... }:

let
  pythonEnv = pkgs.python312.withPackages (ps: [
    ps.pygame
  ]);
in
{
  # Put this Python (with pygame) in your shell
  packages = [
    pythonEnv
  ];

  # Optional but nice: make sure `python` is that interpreter
  env.PYTHON = "${pythonEnv}/bin/python";
}
