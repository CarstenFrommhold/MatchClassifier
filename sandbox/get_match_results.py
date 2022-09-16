import os
import sys
import time

# seasons = ["9394", "9495", "9596", "9697", "9798", "9900", "0001", "0102", "0203",
# "0304", "0405", "0506", "0607", "0708", "0809", "0910", "1011", "1112", "1213",
# "1314", "1415", "1516", "1617", "1718", "1819", "1920", "2021", "2122"]

seasons = ["2122"]

for season in seasons:

    matches = f'https://www.football-data.co.uk/mmz4281/{season}/D1.csv'
    os.system(f"echo download {matches}")
    if sys.platform == "darwin":  # macos
        os.system(f"curl -o s_{season}.csv {matches}")
    else:
        os.system(f"wget {matches} ")
        os.system(f"mv D1.csv s_{season}.csv")
    time.sleep(1)
