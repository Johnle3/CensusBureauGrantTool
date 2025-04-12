#!/usr/bin/env python3
import os
import sys
import json
import shutil
import importlib

def main():
    # ----------------------------------------------------------------------
    # 1. Load config.json
    # ----------------------------------------------------------------------
    config_path = "/Users/johnle/Downloads/DTSP_discover/config.json"
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: config.json not found at {config_path}")
        sys.exit(1)

    # Read the paths from config
    data_pull_dir   = config.get("ACSDataPull_dir")
    env_file_path   = config.get("env_file_path")
    census_repo_dir = config.get("census_repo_path")

    if not data_pull_dir or not env_file_path:
        print("Error: 'ACSDataPull_dir' or 'env_file_path' missing from config.json")
        sys.exit(1)

    # ----------------------------------------------------------------------
    # 2. Prepare the output directory (overwrite if it exists)
    # ----------------------------------------------------------------------
    if os.path.exists(data_pull_dir):
        print(f"Overwriting existing directory: {data_pull_dir}")
        shutil.rmtree(data_pull_dir)
    os.makedirs(data_pull_dir, exist_ok=True)
    print(f"Data will be saved to: {data_pull_dir}")

    # ----------------------------------------------------------------------
    # 3. Load the API key
    # ----------------------------------------------------------------------
    api_key = os.getenv("CENSUS_API_KEY")
    if not api_key:
        # fallback to env.txt
        try:
            with open(env_file_path, "r") as f:
                content = f.read().strip()
                if '=' in content:
                    _, api_key = content.split("=", 1)
                else:
                    api_key = content
                api_key = api_key.strip().strip('"')
        except FileNotFoundError:
            print("Error: CENSUS_API_KEY not set and env.txt not found")
            sys.exit(1)

    if not api_key:
        print("Error: API key is empty.")
        sys.exit(1)
    print("Using API key:", api_key)

    # ----------------------------------------------------------------------
    # 4. Add local census-data-downloader repo to PYTHONPATH
    # ----------------------------------------------------------------------
    if census_repo_dir and os.path.isdir(census_repo_dir):
        sys.path.insert(0, census_repo_dir)
        print(f"Added census-data-downloader repo to PYTHONPATH: {census_repo_dir}")
    else:
        print("Warning: census_repo_path not set or not a directory. Using installed package if available.")

    # ----------------------------------------------------------------------
    # 5. Dynamically import each table class
    # ----------------------------------------------------------------------
    table_class_names = [
        "AgeDownloader", "AncestryDownloader", "DisabilityDownloader",
        "DisabilitypovertyDownloader", "CognitivedifficultyDownloader",
        "EducationDownloader", "EducationshortDownloader",
        "EmploymentstatusDownloader", "ForeignbornDownloader",
        "CitizenstatusDownloader", "GiniDownloader", "HousingvalueDownloader",
        "MedianmonthlyhousingcostsDownloader", "MedianhousingvalueDownloader",
        "MediangrossrentDownloader", "TenurepopDownloader", "TenureDownloader",
        "TenurelatinoDownloader", "TenurewhiteDownloader", "TenureblackDownloader",
        "TenureasianDownloader", "MediangrossrentbybedroomDownloader",
        "GrossrentbybedroomDownloader", "HouseholdincomeDownloader",
        "HouseholdincomelatinoDownloader", "HouseholdincomewhiteDownloader",
        "HouseholdincomeblackDownloader", "HouseholdincomeasianDownloader",
        "InternetDownloader", "HouseholdlanguageDownloader",
        "LanguageshortformDownloader", "LanguagelongformDownloader",
        "LatinoDownloader", "MedianageDownloader",
        "MedianhouseholdincomeDownloader",
        "MedianhouseholdincomelatinoDownloader",
        "MedianhouseholdincomewhiteDownloader",
        "MedianhouseholdincomeblackDownloader",
        "MedianhouseholdincomeasianDownloader", "MobilityDownloader",
        "MobilitybysexDownloader", "MobilitywhiteDownloader",
        "MobilityblackDownloader", "MobilityasianDownloader",
        "MobilitylatinoDownloader", "MobilitybycitizenshipDownloader",
        "OccupancyDownloader", "PercapitaincomeDownloader",
        "PercapitaincomelatinoDownloader", "PercapitaincomewhiteDownloader",
        "PercapitaincomeblackDownloader", "PercapitaincomeasianDownloader",
        "PopulationDownloader", "PovertyDownloader",
        "PovertystatusbygenderDownloader", "PovertystatusbyageDownloader",
        "PovertylatinoDownloader", "PovertywhiteDownloader",
        "PovertyblackDownloader", "PovertyasianDownloader",
        "RaceDownloader", "AianaloneorincomboDownloader", "AsianDownloader",
        "SnapDownloader", "SnaplatinoDownloader", "SnapwhiteDownloader",
        "SnapblackDownloader", "SnapasianDownloader", "VeteransDownloader",
        "YearstructurebuiltDownloader", "AgehouseholderbyyearbuiltDownloader",
        "TenurebyyearbuiltDownloader", "VotersDownloader",
    ]

    downloaded_classes = []
    for name in table_class_names:
        try:
            tbl_mod = importlib.import_module("census_data_downloader.tables")
            cls = getattr(tbl_mod, name)
            downloaded_classes.append(cls)
        except (ImportError, AttributeError):
            print(f"Skipping {name}: not available")

    print("\nWill download these tables:")
    for cls in downloaded_classes:
        print("  -", cls.__name__)

    # ----------------------------------------------------------------------
    # 6. Download data for each class
    # ----------------------------------------------------------------------
    year = 2021  # adjust or make a list if needed
    for cls in downloaded_classes:
        print(f"\n=== {cls.__name__} ===")
        try:
            dl = cls(api_key=api_key, data_dir=data_pull_dir, years=year)
            if hasattr(dl, "download_states"):
                print("  downloading states…")
                dl.download_states()
            if hasattr(dl, "download_counties"):
                print("  downloading counties…")
                dl.download_counties()
            # add more geographies here if desired
        except Exception as e:
            print(f"Error in {cls.__name__}: {e}")

    print("\nAll done! Check your CSVs in:", data_pull_dir)

if __name__ == "__main__":
    main()
