import os
import argparse
import logging
import pandas as pd
import fcc_area_query
import combine_csv
import clean_fcc
import spatial_join
import bbn_scraper
import join_bbn_with_spatial
import datetime
from tqdm import tqdm


def main(county_fip, output_dir):
    # Try making some temporary directories to store information
    logging.debug("County fip: %s" % county_fip)

    bbn_name = (
        "%s_%s_broadband_prices.csv.xz" % (county_fip, datetime.date.today().year),
    )

    os.system("mkdir -p %s" % output_dir)
    os.system("mkdir -p temp_bbn")

    os.system(
        "python fcc_area_query.py -i %s -o temp_fcc -f"
        % os.path.join(output_dir, "%s.csv.xz" % county_fip)
    )
    os.system(
        "python combine_csv.py -i temp_fcc -o %s -f"
        % os.path.join(output_dir, "%s_geocoded.csv.xz" % county_fip)
    )

    # Download county shapefiles
    os.system(
        "wget -nc -P %s https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/TABBLOCK/2020/tl_2020_%s_tabblock20.zip"
        % (output_dir, county_fip)
    )

    # Clean downloaded fcc data
    os.system(
        "python clean_fcc.py -i %s -o %s -f"
        % (
            os.path.join(output_dir, "%s_geocoded.csv.xz" % county_fip),
            os.path.join(output_dir, "%s_cleaned.csv.xz" % county_fip),
        )
    )

    # Spatiall join the cleaned data with the shapefiles
    os.system(
        "python spatial_join.py -i %s -s %s -c %s -o %s -f"
        % (
            os.path.join(output_dir, "%s_cleaned.csv.xz" % county_fip),
            os.path.join(output_dir, "tl_2020_%s_tabblock20.zip" % county_fip),
            "%s" % county_fip,
            os.path.join(output_dir, "%s_spatial_joined.csv.xz" % county_fip),
        )
    )

    # Query broadbandnow
    os.system(
        "python bbn_scraper.py -i %s -c street -o %s -l -c address"
        % (
            os.path.join(output_dir, "%s_spatial_joined_csv.xz" % county_fip),
            "temp_%s_bbn/" % (county_fip),
        )
    )

    os.system(
        "python combine_csv.py -i %s -o %s -f"
        % (
            os.path.join("temp_%s_bbn/", "%s.cxv.xz" % county_fip),
            os.path.join(
                output_dir,
                "%s_%s_broadband_prices.csv.xz"
                % (county_fip, datetime.date.today().year),
            ),
        )
    )

    os.system(
        "python join_bbn_with_spatial.py -i %s -s %s -o %s -c %s"
        % (
            os.path.join(
                output_dir,
                "%s_%s_broadband_prices.csv.xz"
                % (county_fip, datetime.date.today().year),
            ),
            os.path.join(output_dir, "%s_spatial_joined.xxsc.xz" % county_fip),
            os.path.join(output_dir, "%s_bbn_space_joined.csv.xz" % county_fip),
            "%s" % county_fip,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given csv(s) with address information, return a cleaned broadbandnow csv with geometry that can be visualized"
    )
    parser.add_argument(
        "-i",
        "--input_county_fips",
        nargs="+",
        help="A list of county fip(s) to filter from the database",
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

    args = parser.parse_args()
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)

    for fip in args.input_county_fips:
        assert len(fip) == 5, "[%s] not 5 characters long" % (fip)
    assert os.path.isdir(args.output_dir), "output dir is invalid: %s" % args.output_dir

    pbar = tqdm(args.input_county_fips)
    for fip in pbar:
        pbar.set_description("Parsing: %s" % fip)
        try:
            main(
                fip,
                args.output_dir,
            )
        except KeyboardInterrupt:
            print("Interrupted")
            break
