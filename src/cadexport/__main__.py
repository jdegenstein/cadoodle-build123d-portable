"""
A command-line tool to export a specific build123d object from a user-provided
script to an STL file.
"""
import argparse
import sys
from pathlib import Path
from build123d import export_stl, Shape


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        prog="python -m cadexport",
        description="A utility to export a build123d variable from a Python script to an STL file.",
    )
    parser.add_argument(
        "script_path",
        type=str,
        help="Path to the Python script containing the build123d object.",
    )
    parser.add_argument(
        "variable_name",
        type=str,
        help="The name of the variable in the script that holds the object to be exported. Defaults to 'p'.",
        default="p",
    )
    parser.add_argument(
        "output_filename",
        type=str,
        help="The desired name for the output STL file (e.g., 'model.stl').",
    )

    args = parser.parse_args()

    script_path = Path(args.script_path)
    output_path = Path(args.output_filename)

    # --- Validate Script Path ---
    if not script_path.is_file():
        print(f"Error: Script file not found at '{script_path}'", file=sys.stderr)
        sys.exit(1)

    # --- Execute User Script in a Controlled Scope ---
    print(f"INFO: Reading and executing script '{script_path}'...")
    script_globals = {}
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            script_code = f.read()
        # By providing script_globals, we capture all top-level variables from the script
        exec(script_code, script_globals)
    except Exception as e:
        print(
            f"Error: An exception occurred while executing '{script_path}':\n{e}",
            file=sys.stderr,
        )
        sys.exit(1)

    # --- Extract the Target Variable ---
    if args.variable_name not in script_globals:
        print(
            f"Error: Variable '{args.variable_name}' was not found in the script '{script_path}'.",
            file=sys.stderr,
        )
        print(
            "Please ensure the variable is defined at the top level of the script.",
            file=sys.stderr,
        )
        sys.exit(1)

    cad_object = script_globals[args.variable_name]

    # --- Export to STL ---
    try:
        print(f"INFO: Exporting '{args.variable_name}' to '{output_path}'...")
        if hasattr(cad_object, "part"):
            export_stl(cad_object.part, str(output_path))
        else:
            export_stl(cad_object, str(output_path))
        print(f"\nSuccess! Your model has been saved to '{output_path.resolve()}'")
    except Exception as e:
        print(f"Error: Failed to export the object to STL:\n{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
