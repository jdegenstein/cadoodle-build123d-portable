# cadoodle-build123d-portable

The purpose of this repository is to generate (with github workflows) fully portable archives that contain build123d (and possibly other supporting packages like ocp_vscode). These fully portable archives contain (1) fully working python, (2) uv, (3) build123d and dependencies, (4) other related packages.

This repository also contains some python tooling to assist in integrating build123d with cadoodle with the bundled package `build123d_cli`. The artifacts are tar.gz on Linux to preserve permissions, .zip on macos, and self extracting executable (.exe) on Windows. Windows uses a self extracting executable to ensure that long path limitations of the built-in unzipping tool do not prevent extracting all the files (user reported issue).

How to test on linux/mac:
```sh
py/bin/python -m build123d_cli py_gearworks SpurGear --number-of-teeth 23 export_directory ./
```

How to test on windows:
```sh
py\python -m build123d_cli py_gearworks SpurGear --number-of-teeth 23 export_directory .\
```

JSON schema examples (linux/mac):
```sh
py/bin/python -m build123d_cli --json-schema
py/bin/python -m build123d_cli py_gearworks --json-schema
py/bin/python -m run build123d_cli py_gearworks SpurGear --json-schema
```
