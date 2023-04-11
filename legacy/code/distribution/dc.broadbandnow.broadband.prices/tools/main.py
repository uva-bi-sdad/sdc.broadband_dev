import os
import argparse
import logging
import pandas as pd
from core_to_fcc import main as c2f
from fcc_area_query import main as fca
from combine_csv import main as cc

"""
Writing a wrapper that combines everything so that:

Input:
    1) The 5 digit fips code of the county in question, and 
    2) The name of the county

Output:
    1) csv.xz of the broadbandnow results of the county
    2) csv.xz of the spatial joined results of the broadbandnow-available data (for plotting)
    

# mkdir -p temp (a shared directory for all the outputs)
# mkdir -p temp_bbn (to be deleted immediately after joining)

"""


def main(county_fip):
    # c2f(["-f", "/etc/hosts", "-t", "json"])

    # download county shapefiles
    os.system(
        "wget https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/TABBLOCK/2020/tl_2020_%s_tabblock20.zip"
        % county_fip
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given csv(s) with address information, return a cleaned broadbandnow csv with geometry that can be visualized"
    )
    parser.add_argument(
        "-i",
        "--input_files",
        nargs="+",
        help="The input csv(s) with address information",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        help="The output directory where the processed artifacts are dumped",
        required=True,
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

    for file in args.input_files:
        assert os.path.isfile(file), "input file is invalid: %s" % file

        test_df = pd.read_csv(file)
        assert "address" in test_df.columns, "has no address column: %s" % file

    if args.output_file and not args.force:
        assert not os.path.isfile(args.output_file), "output file is invalid"

    main(
        args.input_files,
        args.output_file,
        args.location,
    )
