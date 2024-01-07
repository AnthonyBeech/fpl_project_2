# FPL MLOps

# Summary
* Project starts with legacy data from github found here [github](https://github.com/vaastav/Fantasy-Premier-League)
    * Only game week data per player is used for now
* To recreate intial legacy data, run:
    * src/pipeline/extract_legacy_data.py
        * Make sure to save the legacy data according to your setup in the config.YAML file
* Each Sunday at midnight, the extraction api script will run to ensure that the data is up to date
