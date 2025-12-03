{
  pkgs,
  lib,
  ...
}:

let
  buildInputs = with pkgs; [
    stdenv.cc.cc
    libuv
    zlib
    SDL2
    SDL2_image
    SDL2_mixer
    SDL2_ttf
    wayland
    xorg.libX11
    xorg.libXcursor
    xorg.libXrandr
    xorg.libXi
  ];
in
{
  env = {
    LD_LIBRARY_PATH = "${lib.makeLibraryPath buildInputs}";
  };

  languages.python = {
    enable = true;
    venv = {
      enable = true;
    };
  };

  enterShell = ''
    . .devenv/state/venv/bin/activate

    # Create a symlink to the Python virtual environment for IDE compatibility
    if [ ! -L "$DEVENV_ROOT/venv" ]; then
        ln -s "$DEVENV_STATE/venv/" "$DEVENV_ROOT/venv"
    fi
  '';
}

