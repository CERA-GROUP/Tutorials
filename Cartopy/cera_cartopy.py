# Geospatial data processing and producing maps
# CERA Group, Louisiana State University
# Website: https://cera.coastalrisk.live
# Github: https://github.com/CERA-GROUP

# This script is the command-line companion to the Cartopy notebook. It keeps
# the tutorial flow visible while separating input checks, data loading, and
# plotting into small functions that are easier to test and reuse.

import argparse
from pathlib import Path
import urllib.request
import warnings


# Shared tutorial settings are constants so map bounds, titles, and required
# CSV columns are defined once and stay consistent across the script.
ATLANTIC_GULF_EXTENT = [-120, -45, 5, 50]
DEFAULT_TITLE = "Background map with water level stations"
LOGO_URL = "https://coastalrisk.live/wp-content/uploads/2018/05/cera_50x50.png"
REQUIRED_COLUMNS = ("station_id", "lat", "lon")


def parse_args():
    """Parse command-line options for the Cartopy tutorial script."""
    # argparse gives the script standard help text and clear errors for missing
    # or misspelled command-line options.
    parser = argparse.ArgumentParser(
        description="Create Cartopy maps from a CSV file of station coordinates."
    )
    parser.add_argument(
        "csv_file",
        type=Path,
        help="CSV file containing station_id, lat, and lon columns.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Save the final station map to this image file.",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Do not open interactive plot windows.",
    )
    parser.add_argument(
        "--title",
        default=DEFAULT_TITLE,
        help="Title for the final station map.",
    )
    return parser.parse_args()


def validate_csv(path):
    """Check that the CSV path exists and can be read."""
    # File checks happen before loading data or plotting libraries, so common
    # user mistakes fail with a direct message.
    if not path.exists():
        raise ValueError(f"CSV file not found: {path}")
    if not path.is_file():
        raise ValueError(f"CSV path is not a file: {path}")

    try:
        with path.open("r", encoding="utf-8"):
            pass
    except OSError as exc:
        raise ValueError(f"CSV file is not readable: {path}") from exc

    return path


def validate_output_path(path):
    """Check that the output directory exists before plotting."""
    if path is None:
        return None

    # Matplotlib can create the image file, but it will not create missing
    # parent folders. Catch that early and report the exact directory problem.
    output_dir = path.parent
    if output_dir and not output_dir.exists():
        raise ValueError(f"Output directory does not exist: {output_dir}")

    return path


def load_station_data(path):
    """Load and validate station coordinate data."""
    # Import pandas here so path validation can still run in minimal
    # environments and report missing files without needing plotting packages.
    import pandas as pd

    try:
        # Station IDs may contain leading zeros, so keep them as text for labels.
        stations = pd.read_csv(path, dtype={"station_id": str})
    except Exception as exc:
        raise ValueError(f"Could not read CSV file: {path}") from exc

    # The plotting functions rely on these three columns. Failing here avoids
    # harder-to-debug errors later in Cartopy or Matplotlib.
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in stations.columns
    ]
    if missing_columns:
        raise ValueError(
            "CSV file is missing required column(s): "
            + ", ".join(missing_columns)
        )

    if stations.empty:
        raise ValueError("CSV file does not contain any station rows.")

    for coordinate in ("lat", "lon"):
        # Convert coordinates once after loading, then keep the DataFrame clean
        # for all downstream plotting functions.
        numeric_values = pd.to_numeric(stations[coordinate], errors="coerce")
        invalid_rows = numeric_values.isna()
        if invalid_rows.any():
            # Add 2 because pandas indices are zero-based and CSV row 1 is the
            # header line.
            row_numbers = stations.index[invalid_rows][:5] + 2
            rows_text = ", ".join(str(row) for row in row_numbers)
            raise ValueError(
                f"Column '{coordinate}' must contain numeric values. "
                f"Invalid data found on CSV row(s): {rows_text}"
            )
        stations[coordinate] = numeric_values

    return stations


def create_overview_maps(show=True):
    """Create the simple overview maps used in the tutorial."""
    # These maps mirror the early notebook examples and introduce projections
    # before station data is added.
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import matplotlib.pyplot as plt

    print("Creating a basic map with Cartopy - Plate Carree projection")
    # Use a separate figure for each example so closing or showing one plot does
    # not affect the next tutorial step.
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    _show_or_close(fig, show)

    print("Creating a basic map with Cartopy - Mollweide projection")
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(
        1,
        1,
        1,
        projection=ccrs.Mollweide(central_longitude=-90),
    )
    ax.add_feature(cfeature.COASTLINE)
    _show_or_close(fig, show)

    print("Creating a map with customized coastline and a background image")
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE, linestyle="dotted", linewidth=1, color="red")
    ax.stock_img()
    _show_or_close(fig, show)


def create_regional_station_map(stations, show=True):
    """Create a broad Atlantic/Gulf map with station points."""
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt

    print("Adding station points to the regional background map")
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    # Cartopy expects extent as [west, east, south, north]. This broad view
    # provides geographic context before zooming to the station bounding box.
    ax.set_extent(ATLANTIC_GULF_EXTENT, crs=ccrs.PlateCarree())

    _add_map_features(ax, scale="50m")
    _add_gridlines(ax)

    ax.set_title(DEFAULT_TITLE)
    ax.scatter(
        stations["lon"],
        stations["lat"],
        color="red",
        marker="o",
        s=100,
        # The input CSV stores station coordinates as longitude/latitude.
        transform=ccrs.PlateCarree(),
    )
    _show_or_close(fig, show)


def create_station_map(stations, title, output=None, show=True):
    """Create the final labeled station map and optionally save it."""
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt

    print("Creating the final labeled station map")
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # The final map focuses on the provided data rather than a fixed region, so
    # its extent is derived from station coordinates.
    ax.set_extent(_station_extent(stations), crs=ccrs.PlateCarree())
    _add_map_features(ax, scale="10m")
    _add_gridlines(ax)

    ax.set_title(title)
    ax.scatter(
        stations["lon"],
        stations["lat"],
        color="red",
        marker="o",
        s=100,
        # Tell Cartopy that station values are already lon/lat coordinates.
        transform=ccrs.PlateCarree(),
    )

    # Labels are offset slightly so they do not sit directly on top of markers.
    for station in stations.itertuples(index=False):
        ax.text(
            station.lon + 0.2,
            station.lat,
            str(station.station_id),
            transform=ccrs.PlateCarree(),
        )

    _add_cera_logo(ax, stations["lon"].min(), stations["lat"].max())

    if output is not None:
        # Only the final station map is saved; the overview maps remain tutorial
        # demonstrations.
        fig.savefig(output, dpi=150, bbox_inches="tight")
        print(f"Saved final station map to {output}")

    _show_or_close(fig, show)


def _add_map_features(ax, scale):
    """Add common Cartopy background features."""
    import cartopy.feature as cfeature

    # Keeping repeated Natural Earth features in one helper makes the regional
    # and final maps visually consistent.
    ax.add_feature(cfeature.COASTLINE.with_scale(scale), linewidth=0.6)
    ax.add_feature(cfeature.OCEAN.with_scale(scale), color="#EDFBFF")
    ax.add_feature(cfeature.LAND.with_scale(scale), color="#FBF5EA")
    ax.add_feature(cfeature.LAKES.with_scale(scale), color="#EDFBFF")
    ax.add_feature(cfeature.STATES.with_scale(scale), linewidth=0.5)


def _add_gridlines(ax):
    """Add labeled gridlines to a Cartopy axis."""
    gridlines = ax.gridlines(draw_labels=True, linestyle="dotted", color="black")
    # Top and right labels duplicate the bottom and left labels on a simple map.
    gridlines.top_labels = False
    gridlines.right_labels = False


def _station_extent(stations, buffer_degrees=1.0):
    """Return a [west, east, south, north] extent around the stations."""
    # A small buffer keeps markers and labels from touching the map edges.
    west = stations["lon"].min() - buffer_degrees
    east = stations["lon"].max() + buffer_degrees
    south = stations["lat"].min() - buffer_degrees
    north = stations["lat"].max() + buffer_degrees
    return [west, east, south, north]


def _add_cera_logo(ax, lon_min, lat_max):
    """Add the CERA logo when it is reachable."""
    import numpy as np
    from PIL import Image
    from matplotlib.offsetbox import AnnotationBbox, OffsetImage, TextArea

    try:
        # The logo is decorative context. If the network is unavailable, the map
        # should still be produced and the user should see a warning.
        with urllib.request.urlopen(LOGO_URL) as url:
            logo = np.array(Image.open(url))
    except Exception as exc:
        warnings.warn(f"Could not load CERA logo: {exc}")
        return

    imagebox = OffsetImage(logo, zoom=0.5)
    logo_box = AnnotationBbox(
        imagebox,
        (lon_min - 0.6, lat_max + 0.6),
        bboxprops={"edgecolor": "None"},
        frameon=False,
    )
    label_box = AnnotationBbox(
        TextArea("cera.coastalrisk.live"),
        (lon_min + 0.75, lat_max + 0.6),
    )
    ax.add_artist(logo_box)
    ax.add_artist(label_box)


def _show_or_close(fig, show):
    """Show a figure interactively or close it for batch runs."""
    import matplotlib.pyplot as plt

    if show:
        plt.show()
    else:
        # Closing figures in --no-show mode prevents memory growth and avoids
        # opening windows during automated runs.
        plt.close(fig)


def main():
    args = parse_args()
    show_plots = not args.no_show

    try:
        # Validate all user-controlled inputs before spending time on plotting.
        csv_path = validate_csv(args.csv_file)
        output_path = validate_output_path(args.output)
        stations = load_station_data(csv_path)
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}") from exc

    if not show_plots:
        import matplotlib

        # The Agg backend renders images without a GUI, which is useful for
        # servers, scripts, and reproducible command-line runs.
        matplotlib.use("Agg")

    print("Printing the station data frame")
    stations.info()

    # Keep the notebook's learning sequence: simple projection examples first,
    # then a regional station view, and finally the labeled output map.
    create_overview_maps(show=show_plots)
    create_regional_station_map(stations, show=show_plots)
    create_station_map(
        stations,
        title=args.title,
        output=output_path,
        show=show_plots,
    )


if __name__ == "__main__":
    main()
