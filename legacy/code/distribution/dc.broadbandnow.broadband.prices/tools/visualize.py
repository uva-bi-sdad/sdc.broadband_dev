import requests
import numpy as np
import os
import pandas as pd
from tqdm import tqdm
import argparse
import pandas as pd
import requests
from tqdm import tqdm
import math
from io import StringIO
import warnings
import logging
import pathlib
import shutil
import geopandas as gpd
from glob import glob
from shapely import wkt
from matplotlib import pyplot as plt
import contextily as cx


def main(
    input_file,
    output_file,
    location,
):
    warnings.filterwarnings("ignore")
    mdf = pd.read_csv(input_file)
    mdf["geometry"] = mdf["geometry"].apply(wkt.loads)

    gdf = gpd.GeoDataFrame(mdf, crs="epsg:4326")
    gdf_wm = gdf.to_crs(epsg=3857)

    ax = gdf_wm.plot(
        figsize=(10, 10),
        column="price",
        alpha=1,
        markersize=1,
        cmap="plasma",
        legend=True,
    )  # add block outlines
    cx.add_basemap(ax, source=cx.providers.Stamen.TonerLite)
    ax.set_title("Minimum price for 100 Mbps download for %s" % location)
    plt.savefig(output_file)
    logging.info(
        "[%s] File export successful: %s" % (os.path.isfile(output_file), output_file)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given a geopandas file, generate a plot"
    )

    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        help="The input csv with broadbandnow results",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        help="The output csv where matches are found",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--location",
        type=str,
        help="Optional location appendix to the title",
        required=False,
        default="",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Show debugging outputs",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-f",
        "--force",
        action=argparse.BooleanOptionalAction,
        help="Whether or not to override the output file",
        required=False,
        default=False,
    )

    args = parser.parse_args()
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)

    assert os.path.isfile(args.input_file), "input file is invalid"
    test_df = pd.read_csv(args.input_file)
    assert "address" in test_df.columns

    if args.output_file and not args.force:
        assert not os.path.isfile(args.output_file), "output file is invalid"

    main(
        args.input_file,
        args.output_file,
        args.location,
    )