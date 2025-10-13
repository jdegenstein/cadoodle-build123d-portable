from gggears import *
from build123d import *
import fire
from os import PathLike
from pathlib import Path
from datetime import datetime
from bd_warehouse.fastener import HexNut

# Get the current date and time
current_datetime = datetime.now()

# Format the datetime object into a string with the desired components
timestamp_string = current_datetime.strftime("%Y-%m-%d_%H_%M_%S")

print(f"Current timestamp: {timestamp_string}")


def _export_directory(
    self,
    directory: PathLike | str | bytes,
    # tolerance: float = 1e-3,
    # angular_tolerance: float = 0.1,
    # ascii_format: bool = False,
) -> bool:
    base_filename_no_extension = Path("build123d_" + timestamp_string)

    if hasattr(self, "build_part"):
        to_export = self.build_part()
    elif hasattr(self, "part"):
        to_export = self.part
    elif hasattr(self, "wrapped"):
        to_export = self
    else:
        print("unknown part attribute")

    export_stl(to_export, directory / base_filename_no_extension.with_suffix(".stl"))
    svg_exporter = ExportSVG(unit=Unit.MM, line_weight=0.5)
    svg_exporter.add_layer("Layer 1", fill_color=(255, 0, 0), line_color=(0, 0, 255))
    svg_exporter.add_shape(to_export, layer="Layer 1")
    svg_exporter.write(directory / base_filename_no_extension.with_suffix(".svg"))


class_list = [SpurGear, HelicalGear, HexNut]

for cls in class_list:
    # monkeypatch
    cls.export_directory = _export_directory


def main():
    """
    Exposes a nested dictionary of classes to the command line.
    """
    # The nested dictionary creates a multi-level CLI.
    # Top-level commands will be 'services' and 'utils'.
    cli_groups = {
        "gggears": {
            "spurgear": SpurGear,
            "helicalgear": HelicalGear,
        },
        "bd_warehouse": {
            "hexnut": HexNut,
        },
    }
    fire.Fire(cli_groups)


if __name__ == "__main__":
    main()
