import os
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
    

# mkdir -p temp
# mkdir -p temp_bbn

"""


def main(county_fip):
    # c2f(["-f", "/etc/hosts", "-t", "json"])
    pass
    os.system(
        "https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/TABBLOCK/2020/tl_2020_%s_tabblock20.zip"
        % county_fip
    )
