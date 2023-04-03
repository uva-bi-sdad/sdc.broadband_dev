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
import psycopg2
import shutil
from decouple import config

# import traceback


def download_data(county_fips, temp_dir):
    # decouple so that passwords are not stored
    conn = psycopg2.connect(
        dbname=config("dbname"),
        user= config("user"),
        password= config("password"),
        port= config("port"),
        host= config("host"),
    )
    cur = conn.cursor()

    temp_path = os.path.join(temp_dir, "%s.csv" % county_fips)
    # save csv to file given county_fips code
    logging.debug('Using temporary path" %s' % temp_path)

    # example:  \copy (SELECT situs_address,geoid_cnty FROM corelogic_usda WHERE geoid_cnty = '13121') TO '~/13121.csv' CSV header;
    cur.execute(
        "\copy (SELECT situs_address,geoid_cnty FROM %s WHERE geoid_cnty = '%s') TO '%s' CSV header;"
        % (config("dbname"), county_fips, temp_path)
    )
    # sql = "COPY (SELECT * FROM a_table WHERE month=6) TO STDOUT WITH CSV DELIMITER ';'"
    # with open("/mnt/results/month/table.csv", "w") as file:
    #     cur.copy_expert(sql, file)
    logging.debug('File saved to path')
    cur.close()
    conn.close()

    return pd.read_csv(
        temp_path,
    )


def main(county_fip, output_file, temp_dir, force):
    warnings.filterwarnings("ignore")
    state_fips = pd.read_csv(
        "https://raw.githubusercontent.com/uva-bi-sdad/national_address_database/main/data/fips_state.csv",
        dtype={"fips": object},
    )
    state = state_fips[state_fips["fips"] == county_fip[:2]]["state"].values[0]
    state_abbr = (
        state_fips[state_fips["fips"] == county_fip[:2]]["abbr"].values[0].upper()
    )
    county_fips = pd.read_csv(
        "https://github.com/uva-bi-sdad/national_address_database/raw/main/data/fips_county.csv",
        dtype={"fips": object},
    )
    county = county_fips[county_fips["fips"] == county_fip].values[0]

    df = download_data(county_fip, temp_dir)
    df = df.dropna()
    bdf = pd.DataFrame()

    # Clean up the csv and export the results

    bdf["street"] = df["situs_address"].apply(lambda x: x.split(" %s" % state_abbr)[0])
    bdf["county"] = county
    bdf["state"] = state_abbr
    bdf["zip"] = df["situs_address"].apply(lambda x: x.split("%s " % state_abbr)[-1])

    bdf.to_csv(output_file, index=False)
    return os.path.isfile(bdf)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given a corelogic template, convert to a csv that can be queried to the fcc. First downloads raw data into the temporary directory, then transforms it to a cleaned format in the output filepath"
    )
    parser.add_argument(
        "-i",
        "--input_county_fips",
        type=str,
        help="The county fips to filter from the database",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        help="The output csv",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--temp_dir",
        type=str,
        help="The temporary directory to store raw downloaded files",
        default=".temp",
        required=False,
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
        help="Whether or not to override the output file, if it already exists",
        required=False,
        default=False,
    )
    parser.add_argument(
        "-ft",
        "--force_delete_temp",
        action=argparse.BooleanOptionalAction,
        help="Force delete the temporary directory",
        required=False,
        default=False,
    )

    args = parser.parse_args()
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)

    if not args.force:
        assert not os.path.isfile(args.output_file)

    if not args.force_delete_temp:
        assert not os.path.isdir(args.temp_dir), (
            "temporary directory %s already exists" % args.temp_dir
        )
    else:  # Force delete the temporary files
        shutil.rmtree(args.temp_dir)
    os.mkdir(args.temp_dir)

    success = main(args.input_county_fips, args.output_file, args.temp_dir, args.force)
    print("[%s] Output to %s successful" % (success, args.output_file))

    # Cleaning up temporary directory and its contents
    shutil.rmtree(args.temp_dir)
