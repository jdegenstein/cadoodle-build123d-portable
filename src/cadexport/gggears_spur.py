from gggears import *
from build123d import *
import fire
from os import PathLike

def _export_stl(
    self,
    file_path: PathLike | str | bytes,
    tolerance: float = 1e-3,
    angular_tolerance: float = 0.1,
    ascii_format: bool = False,
) -> bool:
    export_stl(self.build_part(), file_path, tolerance, angular_tolerance, ascii_format)
    
SpurGear.export_stl = _export_stl

def main():
    fire.Fire(SpurGear)

if __name__ == "__main__":
    main()
