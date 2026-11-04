# SPDX-License-Identifier: MIT
# Render one ATCF best-track file into a publication-style map.
#
# Command-line companion to cera_single_track.ipynb.

# Copyright (C): Carola Kaiser 2006-2026, Louisiana State University.
# This script is part of the Coastal Emergency Risks Assessment (CERA), a real-time visualization system for storm surge guidance.
# See https://cera.coastalrisk.live. This CERA script is Open Source software; distributed under the MIT License.

# Authors: Carola Kaiser, Efstratios Nikidis

import argparse
import csv
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patheffects as pe
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io

warnings.filterwarnings("ignore", category=cartopy.io.DownloadWarning)


# ---------------------------------------------------------------------------
# Defaults and shared styling
# ---------------------------------------------------------------------------
ATCF_DATETIME_FORMAT = "%Y%m%d%H"
DEFAULT_DAT = Path("bal142024.dat")
DEFAULT_OUTPUT = Path("example_1_plot.png")
DEFAULT_TITLE = "Milton (2024) Best Track"

INTENSITY_STYLES = (
    ("Tropical Depression", 0, 33, "#6b7280"),
    ("Tropical Storm", 34, 63, "#2b8cbe"),
    ("Category 1", 64, 82, "#e6ab02"),
    ("Category 2", 83, 95, "#e67e22"),
    ("Category 3", 96, 112, "#d95f0e"),
    ("Category 4", 113, 136, "#c62828"),
    ("Category 5", 137, float("inf"), "#7b3294"),
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Render one ATCF best-track file into a publication-style map."
    )
    parser.add_argument(
        "dat_file",
        nargs="?",
        type=Path,
        default=DEFAULT_DAT,
        help=f"ATCF best-track file (default: {DEFAULT_DAT}).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Save the map to this image file (default: {DEFAULT_OUTPUT}).",
    )
    parser.add_argument(
        "--title",
        default=DEFAULT_TITLE,
        help=f"Map title (default: {DEFAULT_TITLE}).",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolution for the saved image (default: 300).",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Do not open the interactive plot window.",
    )
    return parser.parse_args()


def validate_input_path(path):
    if not path.exists():
        raise ValueError(f"ATCF file not found: {path}")
    if not path.is_file():
        raise ValueError(f"ATCF path is not a file: {path}")
    return path


def validate_output_path(path):
    if path.parent and not path.parent.exists():
        raise ValueError(f"Output directory does not exist: {path.parent}")
    return path


def parse_coordinate(value: str) -> float:
    """Convert an ATCF tenths-of-a-degree coordinate such as 286N or 969W."""
    match = re.fullmatch(r"(\d+)([NSEW])", value.strip().upper())
    if not match:
        raise ValueError(f"Invalid ATCF coordinate: {value!r}")
    magnitude = int(match.group(1)) / 10.0
    return -magnitude if match.group(2) in {"S", "W"} else magnitude


def load_atcf_track(dat_path: Path) -> pd.DataFrame:
    """Load the core fields from an ATCF best-track file."""
    parsed_rows = []
    with dat_path.open(newline="", encoding="utf-8") as handle:
        for line_number, fields in enumerate(csv.reader(handle), start=1):
            fields = [field.strip() for field in fields]
            if not fields or all(not field for field in fields):
                continue
            if len(fields) < 11:
                raise ValueError(
                    f"{dat_path}:{line_number} has {len(fields)} fields; expected at least 11"
                )
            try:
                parsed_rows.append(
                    {
                        "basin": fields[0],
                        "storm_number": fields[1],
                        "time": pd.to_datetime(fields[2], format=ATCF_DATETIME_FORMAT, errors="raise"),
                        "technique": fields[4],
                        "latitude": parse_coordinate(fields[6]),
                        "longitude": parse_coordinate(fields[7]),
                        "vmax_kt": pd.to_numeric(fields[8], errors="coerce"),
                        "pressure_hpa": pd.to_numeric(fields[9], errors="coerce"),
                        "status": fields[10],
                    }
                )
            except ValueError as exc:
                raise ValueError(f"{dat_path}:{line_number}: {exc}") from exc

    track = pd.DataFrame(parsed_rows)
    if track.empty:
        raise ValueError(f"No track records found in {dat_path}")

    # ATCF files may repeat a timestamp for different wind-radii records; those
    # share a center position, so one point per advisory is enough here.
    track = (
        track.sort_values("time")
        .drop_duplicates(subset=["time"], keep="first")
        .reset_index(drop=True)
    )
    return track


def padded_extent(track: pd.DataFrame) -> list:
    lon_min = float(track["longitude"].min())
    lon_max = float(track["longitude"].max())
    lat_min = float(track["latitude"].min())
    lat_max = float(track["latitude"].max())
    lon_pad = max((lon_max - lon_min) * 0.12, 2.5)
    lat_pad = max((lat_max - lat_min) * 0.12, 2.0)
    return [lon_min - lon_pad, lon_max + lon_pad, lat_min - lat_pad, lat_max + lat_pad]


def intensity_label(vmax_kt) -> str:
    if pd.isna(vmax_kt):
        return "Unknown"
    for label, lower, upper, _color in INTENSITY_STYLES:
        if lower <= vmax_kt <= upper:
            return label
    return "Unknown"


def intensity_color(label: str) -> str:
    for candidate, _lower, _upper, color in INTENSITY_STYLES:
        if label == candidate:
            return color
    return "#9ca3af"


def add_base_features(ax) -> None:
    """Apply the same Natural Earth visual language as the station-map notebook."""
    ax.add_feature(cfeature.OCEAN.with_scale("10m"), facecolor="#D8DBDE", zorder=0)
    ax.add_feature(cfeature.LAND.with_scale("10m"), facecolor="#FFFFFF", zorder=0)
    ax.add_feature(cfeature.LAKES.with_scale("10m"), facecolor="#D8DBDE",
                   edgecolor="#A8A8A8", linewidth=0.25, zorder=1)
    ax.add_feature(cfeature.RIVERS.with_scale("10m"), edgecolor="#A8A8A8",
                   linewidth=0.22, alpha=0.75, zorder=1)
    ax.add_feature(cfeature.COASTLINE.with_scale("10m"), edgecolor="#A8A8A8",
                   linewidth=0.45, alpha=0.65, zorder=2)
    ax.add_feature(cfeature.BORDERS.with_scale("10m"), edgecolor="#CFCFCF",
                   linewidth=0.30, alpha=0.55, zorder=2)
    ax.add_feature(cfeature.STATES.with_scale("10m"), edgecolor="#CFCFCF",
                   linewidth=0.30, alpha=0.55, zorder=2)


def plot_track_map(dat_path: Path, output: Path, title: str, dpi: int, show: bool = True) -> Path:
    """Render one ATCF best-track file into a publication-style map."""
    track = load_atcf_track(dat_path)
    track["intensity"] = track["vmax_kt"].map(intensity_label)

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "axes.titlesize": 14,
        "legend.fontsize": 8,
    })

    projection = ccrs.PlateCarree()
    fig = plt.figure(figsize=(9.2, 6.8), constrained_layout=False)
    ax = fig.add_axes([0.05, 0.085, 0.72, 0.78], projection=projection)
    ax.set_extent(padded_extent(track), crs=projection)
    add_base_features(ax)

    ax.gridlines(draw_labels=False, linewidth=0.28, color="#9aa5ad",
                 alpha=0.42, linestyle=(0, (2, 3)))

    for spine in ax.spines.values():
        spine.set_linewidth(0.55)
        spine.set_edgecolor("#4b5563")

    line = ax.plot(
        track["longitude"], track["latitude"], transform=projection,
        color="#334155", linewidth=1.65, alpha=0.92, zorder=5,
    )[0]
    line.set_path_effects([pe.Stroke(linewidth=3.2, foreground="white", alpha=0.8), pe.Normal()])

    present_labels = []
    for label, _lower, _upper, color in INTENSITY_STYLES:
        group = track[track["intensity"] == label]
        if group.empty:
            continue
        present_labels.append(label)
        ax.scatter(
            group["longitude"], group["latitude"], transform=projection, s=80, marker="o",
            facecolor=color, edgecolor="white", linewidth=0.6, alpha=0.96, zorder=6,
            path_effects=[pe.withStroke(linewidth=1.1, foreground="#263238", alpha=0.28)],
        )

    start = track.iloc[0]
    end = track.iloc[-1]
    ax.scatter([start["longitude"]], [start["latitude"]], transform=projection, s=72,
               marker="o", facecolor="none", edgecolor="#166534", linewidth=1.5, zorder=7)
    ax.scatter([end["longitude"]], [end["latitude"]], transform=projection, s=58,
               marker="X", facecolor="#111827", edgecolor="white", linewidth=0.55, zorder=7)

    max_wind = track["vmax_kt"].max()
    min_pressure = track.loc[track["pressure_hpa"] > 0, "pressure_hpa"].min()
    max_wind_text = "n/a" if pd.isna(max_wind) else f"{int(max_wind)} kt"
    pressure_text = "n/a" if pd.isna(min_pressure) else f"{int(min_pressure)} hPa"

    fig.text(0.50, 0.830, title, ha="center", va="center", fontsize=18,
             fontweight="bold", color="#111827")
    fig.text(0.50, 0.785,
             f"Advisories: {len(track)} \u00b7 Max wind: {max_wind_text} \u00b7 Min pressure: {pressure_text}",
             ha="center", va="center", fontsize=11.5, color="#4b5563")

    intensity_handles = [
        mlines.Line2D([], [], marker="o", linestyle="None", markersize=6.2,
                      markerfacecolor=intensity_color(label), markeredgecolor="white",
                      markeredgewidth=0.55, label=label)
        for label in present_labels
    ]
    endpoint_handles = [
        mlines.Line2D([], [], marker="o", linestyle="None", markersize=7,
                      markerfacecolor="none", markeredgecolor="#166534",
                      markeredgewidth=1.25, label="Track start"),
        mlines.Line2D([], [], marker="X", linestyle="None", markersize=6.5,
                      markerfacecolor="#111827", markeredgecolor="white",
                      markeredgewidth=0.5, label="Track end"),
    ]
    ax.legend(
        handles=[*intensity_handles, *endpoint_handles], title="Intensity (1-min wind)",
        loc="lower left", bbox_to_anchor=(1.02, 0.0), borderaxespad=0.0,
        frameon=True, framealpha=0.95, facecolor="white", edgecolor="#d0d5da",
        borderpad=0.5, labelspacing=0.42, handletextpad=0.55, fontsize=8.6,
        title_fontsize=9.0,
    )

    fig.savefig(output, dpi=dpi, facecolor="white")
    print("Saved:", output)
    if show:
        plt.show()
    else:
        plt.close(fig)
    return output


def main():
    args = parse_args()
    try:
        dat_path = validate_input_path(args.dat_file)
        output = validate_output_path(args.output)
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}") from exc

    print("Using:", dat_path)
    plot_track_map(
        dat_path=dat_path,
        output=output,
        title=args.title,
        dpi=args.dpi,
        show=not args.no_show,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
