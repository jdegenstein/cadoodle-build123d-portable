from gggears import *
from build123d import *
import fire

SpurGear.export_stl = export_stl

def main():
    fire.Fire(SpurGear)

if __name__ == "__main__":
    main()
