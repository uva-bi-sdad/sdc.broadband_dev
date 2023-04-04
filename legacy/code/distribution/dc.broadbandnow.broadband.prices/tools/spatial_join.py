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
from glob import glob

# import traceback


def main(input_file, output_dir, county_fips, force):
    warnings.filterwarnings("ignore")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given a csv, create an ouput directory with batched fcc area geocoding queries. Assumes that the csv is already formatted to fcc area api standards. Note if the force flag is false, the process will continue where it left off as long as the ouput_dir is the same."
    )

    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        help="The input csv with lat long columns to sptial join",
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
        "-n",
        "--number_per_block",
        type=int,
        help="The number of values to sample per block",
        required=False,
        default=1,
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
        help="Whether or not to override the output directory files",
        required=False,
        default=False,
    )

    args = parser.parse_args()
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)

    assert os.path.isfile(args.input_file), "input file is invalid"
    if not args.force:
        assert not os.path.isdir(args.output_dir), "output file is invalid"
    assert (
        args.number_per_block > 0
    ), "number of values to sample per block is not greater than 0"

    main(args.input_file, args.output_dir, args.force)
