import fire
import json
import inspect
import sys
from typing import get_type_hints
from pathlib import Path
from datetime import datetime
from os import PathLike

from py_gearworks import *
from build123d import *
from bd_warehouse.fastener import HexNut

# --- SCHEMA GENERATION LOGIC ---


class SchemaGenerator:
    @staticmethod
    def get_metadata(obj):
        """Extracts parameters and docstrings from a class or function."""
        target = obj.__init__ if inspect.isclass(obj) else obj
        sig = inspect.signature(target)
        type_hints = get_type_hints(target)
        doc = inspect.getdoc(obj) or ""

        params = []
        for name, param in sig.parameters.items():
            if name == "self":
                continue

            # Clean up type names (e.g., <class 'int'> -> int)
            hint = type_hints.get(name, param.annotation)
            type_name = getattr(hint, "__name__", str(hint)).replace("typing.", "")

            params.append(
                {
                    "name": name,
                    "type": type_name,
                    "default": (
                        None
                        if param.default is inspect.Parameter.empty
                        else param.default
                    ),
                    "required": param.default is inspect.Parameter.empty,
                }
            )

        return {
            "name": obj.__name__ if hasattr(obj, "__name__") else str(obj),
            "description": doc.split("\n")[0],
            "parameters": params,
        }

    @staticmethod
    def custom_serializer(obj):
        """Handles non-serializable types like Path or Numpy arrays."""
        if isinstance(obj, (Path, PathLike)):
            return str(obj)
        if hasattr(obj, "tolist"):  # Handle numpy arrays/vectors
            return obj.tolist()
        return str(obj)


def patched_fire(component=None, *args, **kwargs):
    """Monkeypatch for fire.Fire to intercept --json-schema."""
    if "--json-schema" in sys.argv:
        # Filter out the flag to find the actual command path
        cmd_path = [arg for arg in sys.argv[1:] if arg != "--json-schema"]

        # Traverse the nested dictionary to find the target class
        current = component
        for step in cmd_path:
            if isinstance(current, dict) and step in current:
                current = current[step]
            else:
                break

        # If we landed on a dict, show all schemas in that group.
        # If a class, show that specific schema.
        if isinstance(current, dict):
            output = {k: SchemaGenerator.get_metadata(v) for k, v in current.items()}
        else:
            output = SchemaGenerator.get_metadata(current)

        print(json.dumps(output, indent=2, default=SchemaGenerator.custom_serializer))
        sys.exit(0)

    return original_fire(component, *args, **kwargs)


original_fire = fire.Fire
fire.Fire = patched_fire

current_datetime = datetime.now()
timestamp_string = current_datetime.strftime("%Y-%m-%d_%H_%M_%S")


def _export_directory(self, directory: PathLike | str | bytes) -> bool:
    base_filename_no_extension = Path("build123d_" + timestamp_string)
    if hasattr(self, "build_part"):
        to_export = self.build_part()
    elif hasattr(self, "part"):
        to_export = self.part
    elif hasattr(self, "wrapped"):
        to_export = self
    else:
        print("unknown part attribute")
        return False

    export_stl(to_export, directory / base_filename_no_extension.with_suffix(".stl"))
    svg_exporter = ExportSVG(unit=Unit.MM, line_weight=0.5)
    svg_exporter.add_layer("Layer 1", fill_color=(255, 0, 0), line_color=(0, 0, 255))
    svg_exporter.add_shape(to_export, layer="Layer 1")
    svg_exporter.write(directory / base_filename_no_extension.with_suffix(".svg"))
    return True


pgw_class_list = [
    BevelGear,
    CycloidGear,
    HelicalGear,
    HelicalRack,
    InvoluteRack,
    SpurGear,
    SpurRingGear,
]
bdw_class_list = [HexNut]


def monkeypatch_expdir(class_list):
    for cls in class_list:
        cls.export_directory = _export_directory


monkeypatch_expdir(pgw_class_list)
monkeypatch_expdir(bdw_class_list)

pgw_dict = {cls.__name__: cls for cls in pgw_class_list}
bdw_dict = {cls.__name__: cls for cls in bdw_class_list}


def main():
    cli_groups = {
        "py_gearworks": pgw_dict,
        "bd_warehouse": bdw_dict,
    }
    fire.Fire(cli_groups)


if __name__ == "__main__":
    main()
