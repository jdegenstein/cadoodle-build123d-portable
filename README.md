# cadoodle-build123d-portable

The purpose of this repository is to generate (with github workflows) fully portable archives that contain build123d (and possibly other supporting packages like ocp_vscode). These fully portable archives contain (1) fully working python, (2) uv, (3) build123d and dependencies, (4) other related packages.

Because of limitations in the way that python virtual environments can be moved, I have also included a script `path_patch.[sh/bat]` that will patch the necessary path in `.venv/pyvenv.cfg` with the correct path. In order for these archives to work this script must be ran after the archive is unzipped AND anytime the folder is moved.

This repository may also eventually contain some python tooling to assist in integrating build123d with cadoodle.

How to test on linux/mac:
```sh
chmod +x path_patch.sh
./path_patch.sh
uv/uv run gggears --number-of-teeth=13 export_stl "some_test_filename.stl"
```

How to test on windows:
```sh
path_patch.bat
uv\uv.exe run gggears --number-of-teeth=13 export_stl "some_test_filename.stl"
```
