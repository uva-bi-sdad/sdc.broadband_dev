# Broadbandnow tools

Theoretically, one should be able to accomplish the entire series of tasks without need to write a single line of python code. The main goal is that people can call the toolkit functions and end up with the same data set


## Example steps to parsing Fulton County 13121

1. `python core_to_fcc.py -i 13121 -o temp/13121.csv.xz -ft` Get the addresses given a county fips from corelogic
2. `python fcc_area_query.py -i temp/13121.csv.xz -o temp_fcc -f` Use those address and cross match with fcc area api
3. `python combine_csv.py -i temp_fcc -o temp/13121_geocoded.csv.xz` Combine the files in the ouput address database into a single file
4. `python bbn_scraper.py -i temp/13121_geocoded.csv.xz -c street -o ../../../../data/dc.broadbandnow.broadband.prices/13121_bbn -l -c street` Scrape broadbandnow and export the data to a folder
