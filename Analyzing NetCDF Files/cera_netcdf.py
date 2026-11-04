# SPDX-License-Identifier: MIT
# Inspect and summarize an ADCIRC NetCDF file.
#
# Command-line companion to cera_netcdf.ipynb.

# Copyright (C): Carola Kaiser 2006-2026, Louisiana State University.
# This script is part of the Coastal Emergency Risks Assessment (CERA), a real-time visualization system for storm surge guidance.
# See https://cera.coastalrisk.live. This CERA script is Open Source software; distributed under the MIT License.

import argparse
import sys
from pathlib import Path

import netCDF4
import numpy as np


DEFAULT_INFILE = Path("maxele.63.nc")
DEFAULT_OUTPUT = Path("output_netcdf.txt")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Inspect and summarize an ADCIRC NetCDF file."
    )
    parser.add_argument(
        "-i",
        "--infile",
        type=Path,
        default=DEFAULT_INFILE,
        help=f"NetCDF input file (default: {DEFAULT_INFILE}).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Text report output file (default: {DEFAULT_OUTPUT}).",
    )
    return parser.parse_args()


def build_report(path: Path) -> str:
    """Build a readable summary of the NetCDF dataset."""
    lines: list[str] = [f"File: {path}", ""]

    with netCDF4.Dataset(path) as dataset:
        lines.extend(["Dataset:", str(dataset), ""])
        lines.append("Variables: " + ", ".join(dataset.variables))
        lines.append("")

        for name, variable in dataset.variables.items():
            lines.append(f"Variable: {name}")
            lines.append(str(variable))
            lines.append("")

        lines.append("Dimensions:")
        for name, dimension in dataset.dimensions.items():
            lines.append(f"  {name}: {len(dimension)}")
        lines.append("")

        lines.append("Variable shapes:")
        for name, variable in dataset.variables.items():
            lines.append(f"  {name}: {variable.shape}")
        lines.append("")

        if "x" in dataset.variables:
            x = np.asarray(dataset.variables["x"][:]).ravel()
            lines.append(f"x values: {len(x)} (first: {x[0] if len(x) else 'n/a'})")
        if "y" in dataset.variables:
            y = np.asarray(dataset.variables["y"][:]).ravel()
            lines.append(f"y values: {len(y)} (first: {y[0] if len(y) else 'n/a'})")
        if "element" in dataset.variables:
            element = np.asarray(dataset.variables["element"][:])
            lines.append(f"element shape: {element.shape}")
            if element.size:
                lines.append(f"first element row: {element[0].tolist()}")
        lines.append("")

        if "zeta_max" in dataset.variables:
            zeta = np.asarray(dataset.variables["zeta_max"][:]).ravel()
            if zeta.size:
                lines.append(f"zeta_max range: {np.nanmin(zeta):.4f} to {np.nanmax(zeta):.4f}")
                selected = np.intersect1d(
                    np.where(zeta < 0.6)[0],
                    np.where(zeta > 0.5)[0],
                )
                lines.append(f"zeta_max values between 0.5 and 0.6: {len(selected)}")
            else:
                lines.append("zeta_max is empty")

    return "\n".join(lines)


def main():
    args = parse_args()
    if not args.infile.is_file():
        raise SystemExit(f"Error: input file not found: {args.infile}")

    report = build_report(args.infile)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")

    print("Using:", args.infile)
    print("Saved:", args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
