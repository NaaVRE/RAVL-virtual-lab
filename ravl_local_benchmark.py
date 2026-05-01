# %% Extra libraries for benchmarking
import time

# Extra Libraries

start_time_import_extra_libraries = time.time()
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor  # Multiprocessing
import psutil

end_time_import_extra_libraries = time.time()
elapsed_time_import_extra_libraries = (
    end_time_import_extra_libraries - start_time_import_extra_libraries
)
# %% config
# configuration - v95
start_time_configuration = time.time()

import os
import pathlib
import configparser
import pathlib

config_path = pathlib.Path().home().joinpath(".config/ravl/ravl.conf")
config_parser = configparser.ConfigParser()
config_parser.read(config_path)

conf_minio_user_bucket_name = "naa-vre-user-data"  # the user bucket name
conf_minio_public_bucket_name = "naa-vre-public"  # the public bucket name
conf_minio_public_root_prefix = "vl-vol2bird"
conf_minio_public_conf_prefix = "vl-vol2bird/conf"
conf_minio_public_conf_radar_db_object_name = (
    "vl-vol2bird/conf/OPERA_RADARS_DB.json"
)

conf_minio_endpoint = config_parser.get("scruffy", "endpoint")

### Directories
conf_local_root = "/tmp/data"
conf_local_knmi = "/tmp/data/knmi"
conf_local_odim = "/tmp/data/odim"
conf_local_vp = "/tmp/data/vp"
conf_local_ppi = "/tmp/data/ppi"
conf_local_vpts = "/tmp/data/vpts"
conf_local_conf = "/tmp/data/conf"
conf_local_radar_db = "/tmp/data/conf/OPERA_RADARS_DB.json"
conf_local_visualization_input = "/tmp/data/visualizations/input"
conf_local_visualization_output = "/tmp/data/visualizatons/output"

conf_pvol_output_prefix = "pvol"
conf_vp_output_prefix = "vp"
conf_ppi_output_prefix = "ppi"
conf_vpts_output_prefix = "vpts"
conf_user_directory = "user"

# radar configuration for the KNMI api
# Rewritten in a long format without page breaks. This is to prevent
# the code analyzer to yield an error.
# datasetName, datasetVersion, api_url, radar code (odim)
conf_herwijnen = [
    "radar_volume_full_herwijnen",
    1.0,
    "https://api.dataplatform.knmi.nl/open-data/v1/datasets/radar_volume_full_herwijnen/versions/1.0/files",
    "NL/HRW",
]
conf_denhelder = [
    "radar_volume_full_denhelder",
    2.0,
    "https://api.dataplatform.knmi.nl/open-data/v1/datasets/radar_volume_denhelder/versions/2.0/files",
    "NL/DHL",
]
conf_radars = {
    "hrw": conf_herwijnen,
    "herwijnen": conf_herwijnen,
    "dhl": conf_denhelder,
    "den helder": conf_denhelder,
}

end_time_configuration = time.time()
elapsed_time_configuration = end_time_configuration - start_time_configuration
# %% Secrets
# Secrets
start_time_secrets = time.time()

secret_minio_access_key = config_parser.get("scruffy", "access_key")
secret_minio_secret_key = config_parser.get("scruffy", "secret_key")
secret_key_knmi_api = config_parser.get("knmi", "api_key")

end_time_secrets = time.time()
elapsed_time_secrets = end_time_secrets - start_time_secrets
# %% Param
# Parameters
start_time_parameters = time.time()

param_start_date = "2020-01-07T01:00+00:00"
param_end_date = "2020-01-09T01:00+00:00"
param_maximum_KNMI_files = 192
param_interval_in_minutes = 15
param_radar = "HRW"
param_semaphore = 16  # any int, for ex. 16, or the amount of cores
param_user_email = config_parser.get("user", "username")
param_clean_knmi_input = False
param_upload_results = False
param_clean_pvol_output = True
param_clean_vp_output = True

end_time_parameters = time.time()
elapsed_time_parameters = end_time_parameters - start_time_parameters
# %% initializer
# Initializing
start_time_initializing = time.time()

import pathlib

# Make directories on shared (local) storage
for local_dir in [
    conf_local_root,
    conf_local_knmi,
    conf_local_odim,
    conf_local_vp,
    conf_local_conf,
]:
    local_dir = pathlib.Path(local_dir)
    if not local_dir.exists():
        local_dir.mkdir(parents=True, exist_ok=True)
# Reference files
if not pathlib.Path(conf_local_radar_db).exists():
    from minio import Minio, S3Error

    minioClient = Minio(
        endpoint=conf_minio_endpoint,
        access_key=secret_minio_access_key,
        secret_key=secret_minio_secret_key,
        secure=True,
    )
    print(f"{conf_local_radar_db} not found, downloading")
    minioClient.fget_object(
        bucket_name=conf_minio_public_bucket_name,
        object_name=conf_minio_public_conf_radar_db_object_name,
        file_path=conf_local_radar_db,
    )

# Now produce a variable which acts as a marker for the workflow manager
# We can then drag a line from the configuration / initializer
# and time the start of the rest of the workflow
# If you decide to make different sets of configurations, you can store them
# and decide per workflow which config to attach
init_complete = "Yes"  # Cant sent bool
print("Finished initialization")

end_time_initializing = time.time()
elapsed_time_initializing = end_time_initializing - start_time_initializing
# %%
# list-knmi-files
start_time_listknmi = time.time()

"""
consume dummy var from config to signal workflow start
There is something dodgy going on with how
strings are being passed around.
The string "Yes" is being sent as '"Yes"'
So, to prevent extra quotes being introduced
we eval init_complete first before
we test if it contains "Yes"
"""
# Libraries
import requests


def validate_api_errors():
    if api_response.status_code >= 400:
        raise ValueError(
            f"API {api_response.url} returned an error status code: {api_response.status_code}. {api_response.json()=}"
        )


def validate_number_of_KNMI_files():
    if len(dataset_files) > param_maximum_KNMI_files:
        raise ValueError(
            f"{len(dataset_files)} KNMI files were found to download, but {param_maximum_KNMI_files=}."
            f"\n The data was retrieved with the following parameters:"
            f"\n {param_start_date=} \n {param_end_date=} \n {param_interval_in_minutes=}"
            f"\n Increase {param_maximum_KNMI_files=}, decrease the time range, or increase the interval."
        )


# Strip any extra quotes
init_complete = init_complete.replace("'", "")
init_complete = init_complete.replace('"', "")
if init_complete == "Yes":
    print("Workflow configuration succesfull")
else:
    print("Workflow configuration was not complete, exitting")
    import sys

    sys.exit(1)

# Notes:
# Timestamps in iso8601
# 2020-01-01T00:00+00:00

# configure
start_ts = param_start_date
end_ts = param_end_date
datasetName, datasetVersion, api_url, _ = conf_radars.get(param_radar.lower())
params = {
    "datasetName": datasetName,
    "datasetVersion": datasetVersion,
    "maxKeys": 10,
    "sorting": "asc",
    "orderBy": "created",
    "begin": start_ts,
    "end": end_ts,
}
# Request a response from the KNMI severs
# Try the next page tokens
dataset_files = []
while True:
    api_response = requests.get(
        url=api_url,
        headers={"Authorization": secret_key_knmi_api},
        params=params,
    )
    validate_api_errors()

    api_reponse_json = api_response.json()
    dset_files = api_reponse_json.get("files")

    dset_files = [list(dset_file.values()) for dset_file in dset_files]
    dataset_files += dset_files
    nextPageToken = api_reponse_json.get("nextPageToken")
    if not nextPageToken:
        break
    else:
        params.update({"nextPageToken": nextPageToken})

# KNMI outputs per 5 minutes, per 15 is less of a heavy hit on downloads and processing
# Quick and dirty way to only keep the 15 minute measurements.
# Check API if we can filter for this on their end. If not fine
filtered_list = []
interval_list = list(range(0, 60, param_interval_in_minutes))
for dataset_file in dataset_files:
    minute = int(dataset_file[0].split("_")[-1].split(".")[0][-2:])
    if minute in interval_list:
        filtered_list.append(dataset_file)

dataset_files = filtered_list

validate_number_of_KNMI_files()

print(f"Found {len(dataset_files)} files")
# print(dataset_files)

end_time_listknmi = time.time()
elapsed_time_listknmi = end_time_listknmi - start_time_listknmi
# %% Download KNMI
# Download KNMI files
io_before_download = psutil.disk_io_counters()
start_time_download = time.time()


def download_file(dataset_file):
    filename = dataset_file[0]
    fname_parts = filename.split("_")
    fname_date_part = fname_parts[-1].split(".")[0]
    year = fname_date_part[0:4]
    month = fname_date_part[4:6]
    day = fname_date_part[6:8]
    p = Path(f"{conf_local_knmi}/{radar_code}/{year}/{month}/{day}/{filename}")
    knmi_pvol_paths.append("{}".format(str(p)))

    if not p.exists():
        # print(f"Downloading file {idx}/{n_files}")
        endpoint = f"{api_url}/{filename}/url"
        get_file_response = requests.get(
            endpoint, headers={"Authorization": secret_key_knmi_api}
        )
        download_url = get_file_response.json().get("temporaryDownloadUrl")
        dataset_file_response = requests.get(download_url)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(dataset_file_response.content)
    else:
        # print(f"{p} already exists, skipping")
        pass
    return p


##libraries
import requests
from pathlib import Path
import os

# Changes per 16-11-2023
# Test if we are working with a one element nested list
dataset_files
n_files = len(dataset_files)
print(f"Starting download of {n_files} files.")
_, _, api_url, radar_code = conf_radars.get(param_radar.lower())
knmi_pvol_paths = []
idx = 1
cpu_count = param_semaphore
futures = []
with ProcessPoolExecutor(max_workers=cpu_count) as executor:
    for dataset_file in dataset_files:
        futures.append(executor.submit(download_file, dataset_file))
for future in futures:
    knmi_pvol_paths.append(future.result())
# print(knmi_pvol_paths)
print("Finished downloading files")

# Cast to str
knmi_pvol_paths = [
    knmi_pvol_path.as_posix() for knmi_pvol_path in knmi_pvol_paths
]
end_time_download = time.time()
elapsed_time_download = end_time_download - start_time_download
print(
    f"{param_semaphore=}\tDownloading KNMI files: {elapsed_time_download/60:.0f} minute(s) and {elapsed_time_download%60:.2f} seconds"
)
io_after_download = psutil.disk_io_counters()
io_read_mb_download = (
    io_after_download.read_bytes - io_before_download.read_bytes
) / 1e6
io_write_mb_download = (
    io_after_download.write_bytes - io_before_download.write_bytes
) / 1e6
# %% KNMI-to-ODIM-converter
# KNMI-to-ODIM-converter
"""
notes:
Need to add this such that it can upload the PVOL From this stage
Need to add option such that this can remove the PVOL files from this stage.
Warning, with the removal of PVOL on this stage auto-bricks the VP / RBC gen
We can introduce a flag check where RBC and VP check if PVOL 'needed' to be removed
If that flag is met - abort, there 'shouldnt' be any INPUT files then.
"""
io_before_knmi_convert = psutil.disk_io_counters()
start_time_knmi_convert = time.time()

import subprocess
import pathlib
import h5py
import json
import sys
import shutil

# from typing import List, Object
import math


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise Exception


class FileTranslatorFileTypeError(LookupError):
    """raise this when there's a filetype mismatch derived from h5 file"""


def load_radar_db(radar_db_path):
    """Load and return the radar database

    Output dict sample (wmo code is used as key):
    {
        11038: {'number': '1209', 'country': 'Austria', 'countryid': 'LOWM41', 'oldcountryid': 'OS41', 'wmocode': '11038', 'odimcode': 'atrau', 'location': 'Wien/Schwechat', 'status': '1', 'latitude': '48.074', 'longitude': '16.536', 'heightofstation': ' ', 'band': 'C', 'doppler': 'Y', 'polarization': 'D', 'maxrange': '224', 'startyear': '1978', 'heightantenna': '224', 'diametrantenna': ' ', 'beam': ' ', 'gain': ' ', 'frequency': '5.625', 'single_rrr': 'Y', 'composite_rrr': 'Y', 'wrwp': 'Y'},
        11052: {'number': '1210', 'country': 'Austria', 'countryid': 'LOWM43', 'oldcountryid': 'OS43', 'wmocode': '11052', 'odimcode': 'atfel', 'location': 'Salzburg/Feldkirchen', 'status': '1', 'latitude': '48.065', 'longitude': '13.062', 'heightofstation': ' ', 'band': 'C', 'doppler': 'Y', 'polarization': 'D', 'maxrange': '224', 'startyear': '1992', 'heightantenna': '581', 'diametrantenna': ' ', 'beam': ' ', 'gain': ' ', 'frequency': '5.6', 'single_rrr': 'Y', 'composite_rrr': ' ', 'wrwp': ' '},
        ...
    }
    """
    with open(radar_db_path, mode="r") as f:
        radar_db_json = json.load(f)
    radar_db = {}
    # Reorder list to a usable dict with sub dicts which we can search with wmo codes
    for radar_dict in radar_db_json:
        try:
            wmo_code = int(radar_dict.get("wmocode"))
            radar_db.update({wmo_code: radar_dict})
        except Exception:  # Happens when there is for ex. no wmo code.
            pass
    return radar_db


def translate_wmo_odim(radar_db, wmo_code):
    """ """
    if not isinstance(wmo_code, int):
        raise ValueError("Expecting a wmo_code [int]")
    else:
        pass
    odim_code = (
        radar_db.get(wmo_code).get("odimcode").upper().strip()
    )  # Apparently, people sometimes forget to remove whitespace..
    return odim_code


def extract_wmo_code(in_path):
    with h5py.File(in_path, mode="r") as f:
        # DWD Specific
        # Main attributes
        what = f["what"].attrs
        # Source block
        source = what.get("source")
        source = source.decode("utf-8")
        # Determine if we are dealing with a WMO code or with an ODIM code set
        # Example from Germany where source block is set as WMO
        # what/source: "WMO:10103"
        # Example from The Netherlands where source block is set as a combination of ODIM and various codes
        # what/source: RAD:NL52,NOD:nlhrw,PLC:Herwijnen
        source_list = source.split(sep=",")
    wmo_code = [string for string in source_list if "WMO" in string]
    # Determine if we had exactly one WMO hit
    if len(wmo_code) == 1:
        wmo_code = wmo_code[0]
        wmo_code = wmo_code.replace("WMO:", "")
    # No wmo code found, most likeley dealing with a dutch radar
    elif len(wmo_code) == 0:
        rad_str = [string for string in source_list if "RAD" in string]

        if len(rad_str) == 1:
            rad_str = rad_str[0]
        else:
            print(
                "Something went wrong with determining the rad_str and it wasnt WMO either, exitting"
            )
            sys.exit(1)
        # Split the rad_str
        rad_str_split = rad_str.split(":")
        # [0] = RAD, [1] = rad code
        rad_code = rad_str_split[1]

        rad_codes = {"NL52": "6356", "NL51": "6234", "NL50": "6260"}

        wmo_code = rad_codes.get(rad_code)
    return int(wmo_code)


def translate_knmi_filename(in_path_h5):
    wmo_code = extract_wmo_code(in_path_h5)
    odim_code = translate_wmo_odim(radar_db, wmo_code)
    with h5py.File(in_path_h5, mode="r") as f:
        what = f["what"].attrs
        # Date block
        date = what.get("date")
        date = date.decode("utf-8")
        # Time block
        time = what.get("time")
        # time = f['dataset1/what'].attrs['endtime']
        time = time.decode("utf-8")
        hh = time[:2]
        mm = time[2:4]
        ss = time[4:]
        time = time[:-2]  # Do not include seconds
        # File type
        filetype = what.get("object")
        filetype = filetype.decode("utf-8")
        if filetype != "PVOL":
            raise FileTranslatorFileTypeError("File type was NOT pvol")
    name = [
        odim_code,
        filetype.lower(),
        date + "T" + time,
        str(wmo_code) + ".h5",
    ]
    ibed_fname = "_".join(name)
    return ibed_fname


def knmi_to_odim(in_fpath, out_fpath):
    """
    Converter usage:
    Usage: KNMI_vol_h5_to_ODIM_h5 ODIM_file.h5 KNMI_input_file.h5

    Returns out_fpath and returncode
    """
    converter = "KNMI_vol_h5_to_ODIM_h5"
    command = [converter, out_fpath, in_fpath]
    proc = subprocess.run(command, stderr=subprocess.PIPE)
    output = proc.stderr.decode("utf-8")
    returncode = int(proc.returncode)
    return (out_fpath, returncode, output)


def get_pvol_storage_path(relative_path: str = "") -> str:
    return (
        pathlib.Path(param_user_email)
        .joinpath(conf_pvol_output_prefix)
        .joinpath(relative_path)
    )


def process_knmi_file(
    knmi_path: str, out_path_pvol_odim: str, param_clean_knmi_input
):
    converter_results = knmi_to_odim(
        in_fpath=str(knmi_path), out_fpath=str(out_path_pvol_odim)
    )
    # print(f"{converter_results=}")
    if param_clean_knmi_input:
        pathlib.Path(knmi_path).unlink()
        if not any(pathlib.Path(knmi_path).parent.iterdir()):
            pathlib.Path(knmi_path).parent.rmdir()
    # Determine name for our convention
    ibed_pvol_name = translate_knmi_filename(in_path_h5=out_path_pvol_odim)
    out_path_pvol_odim_tce = pathlib.Path(out_path_pvol_odim).parent.joinpath(
        ibed_pvol_name
    )
    shutil.move(src=out_path_pvol_odim, dst=out_path_pvol_odim_tce)
    return out_path_pvol_odim_tce


# print(f"{knmi_pvol_paths=}")
odim_pvol_paths = []
radar_db = load_radar_db(conf_local_radar_db)
futures = []
with ProcessPoolExecutor(max_workers=cpu_count) as executor:
    for knmi_path in knmi_pvol_paths:
        out_path_pvol_odim = pathlib.Path(knmi_path.replace("knmi", "odim"))
        # print(f"{knmi_path=}")
        # print(f"{out_path_pvol_odim=}")
        if not out_path_pvol_odim.parent.exists():
            out_path_pvol_odim.parent.mkdir(parents=True, exist_ok=False)
        futures.append(
            executor.submit(
                process_knmi_file,
                knmi_path=knmi_path,
                out_path_pvol_odim=str(out_path_pvol_odim),
                param_clean_knmi_input=param_clean_knmi_input,
            )
        )

for future in futures:
    odim_pvol_paths.append(future.result())
end_time_knmi_convert = time.time()
elapsed_time_knmi_convert = end_time_knmi_convert - start_time_knmi_convert
print(
    f"{param_semaphore=}\tKNMI to ODIM took: {elapsed_time_knmi_convert/60:.0f} minute(s) and {elapsed_time_knmi_convert%60:.2f} seconds"
)
io_after_knmi_convert = psutil.disk_io_counters()
io_read_mb_knmi_convert = (
    io_after_knmi_convert.read_bytes - io_before_knmi_convert.read_bytes
) / 1e6
io_write_mb_knmi_convert = (
    io_after_knmi_convert.write_bytes - io_before_knmi_convert.write_bytes
) / 1e6

io_before_pvol_upload = psutil.disk_io_counters()
start_time_pvol_upload = time.time()


def upload_pvol_data(
    conf_minio_user_bucket_name,
    remote_odim_pvol_path,
    odim_pvol_path,
):
    minioClient = Minio(
        endpoint=conf_minio_endpoint,
        access_key=secret_minio_access_key,
        secret_key=secret_minio_secret_key,
        secure=True,
    )
    # check if this exists
    exists = False
    # print(f"Checking if {remote_odim_pvol_path=} exists")
    try:
        _ = minioClient.stat_object(
            bucket_name=(conf_minio_user_bucket_name),
            object_name=remote_odim_pvol_path.as_posix(),
        )
        exists = True
    except:
        pass
    if not exists:
        # print(f"Uploading {odim_pvol_path} to {remote_odim_pvol_path}")
        with open(odim_pvol_path, mode="rb") as file_data:
            file_stat = os.stat(odim_pvol_path)
            minioClient.put_object(
                bucket_name=(conf_minio_user_bucket_name),
                object_name=remote_odim_pvol_path.as_posix(),
                data=file_data,
                length=file_stat.st_size,
            )
    else:
        # print(f"{remote_odim_pvol_path} exists, skipping ")
        pass


# print(f"{odim_pvol_paths=}")

if str2bool(param_upload_results):
    # Minio version
    from minio import Minio

    print(f"Uploading results to {get_pvol_storage_path()}")
    futures = []

    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        for odim_pvol_path in odim_pvol_paths:
            odim_pvol_path = pathlib.Path(odim_pvol_path)
            local_pvol_storage = pathlib.Path(conf_local_odim)
            relative_path = odim_pvol_path.relative_to(local_pvol_storage)
            remote_odim_pvol_path = get_pvol_storage_path(relative_path)
            # print(remote_odim_pvol_path)

            futures.append(
                executor.submit(
                    upload_pvol_data,
                    conf_minio_user_bucket_name=conf_minio_user_bucket_name,
                    remote_odim_pvol_path=remote_odim_pvol_path,
                    odim_pvol_path=odim_pvol_path,
                )
            )

else:
    print(f"{param_upload_results=}")
end_time_pvol_upload = time.time()
elapsed_time_pvol_upload = end_time_pvol_upload - start_time_pvol_upload
print(
    f"{param_semaphore=}\tUploading ODIM PVOL: {elapsed_time_pvol_upload/60:.0f} minute(s) and {elapsed_time_pvol_upload%60:.2f} seconds"
)
io_after_pvol_upload = psutil.disk_io_counters()
io_read_mb_pvol_upload = (
    io_after_pvol_upload.read_bytes - io_before_pvol_upload.read_bytes
) / 1e6
io_write_mb_pvol_upload = (
    io_after_pvol_upload.write_bytes - io_before_pvol_upload.write_bytes
) / 1e6
# cast to string to not break json serializer
odim_pvol_paths = [path.as_posix() for path in odim_pvol_paths]


# %% PVOL-VP-Converter
# PVOL-VP-converter
io_before_pvol_vp = psutil.disk_io_counters()
start_time_pvol_vp = time.time()

import pandas as pd
import re
import pathlib


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise Exception


def load_radar_db(radar_db_path):
    """Load and return the radar database
    Output dict sample (wmo code is used as key):
    {
        11038: {'number': '1209', 'country': 'Austria', 'countryid': 'LOWM41', 'oldcountryid': 'OS41', 'wmocode': '11038', 'odimcode': 'atrau', 'location': 'Wien/Schwechat', 'status': '1', 'latitude': '48.074', 'longitude': '16.536', 'heightofstation': ' ', 'band': 'C', 'doppler': 'Y', 'polarization': 'D', 'maxrange': '224', 'startyear': '1978', 'heightantenna': '224', 'diametrantenna': ' ', 'beam': ' ', 'gain': ' ', 'frequency': '5.625', 'single_rrr': 'Y', 'composite_rrr': 'Y', 'wrwp': 'Y'},
        11052: {'number': '1210', 'country': 'Austria', 'countryid': 'LOWM43', 'oldcountryid': 'OS43', 'wmocode': '11052', 'odimcode': 'atfel', 'location': 'Salzburg/Feldkirchen', 'status': '1', 'latitude': '48.065', 'longitude': '13.062', 'heightofstation': ' ', 'band': 'C', 'doppler': 'Y', 'polarization': 'D', 'maxrange': '224', 'startyear': '1992', 'heightantenna': '581', 'diametrantenna': ' ', 'beam': ' ', 'gain': ' ', 'frequency': '5.6', 'single_rrr': 'Y', 'composite_rrr': ' ', 'wrwp': ' '},
        ...
    }
    """
    with open(radar_db_path, mode="r") as f:
        radar_db_json = json.load(f)
    radar_db = {}
    # Reorder list to a usable dict with sub dicts which we can search with wmo codes
    for radar_dict in radar_db_json:
        try:
            wmo_code = int(radar_dict.get("wmocode"))
            radar_db.update({wmo_code: radar_dict})
        except Exception:  # Happens when there is for ex. no wmo code.
            pass
    return radar_db


def translate_wmo_odim(radar_db, wmo_code):
    """"""
    # class FileTranslatorFileTypeError(LookupError):
    #    '''raise this when there's a filetype mismatch derived from h5 file'''
    if not isinstance(wmo_code, int):
        raise ValueError("Expecting a wmo_code [int]")
    else:
        pass
    odim_code = (
        radar_db.get(wmo_code).get("odimcode").upper().strip()
    )  # Apparently, people sometimes forget to remove whitespace..
    return odim_code


def extract_wmo_code(in_path):
    with h5py.File(in_path, "r") as f:
        # DWD Specific
        # Main attributes
        what = f["what"].attrs
        # Source block
        source = what.get("source")
        source = source.decode("utf-8")
        # Determine if we are dealing with a WMO code or with an ODIM code set
        # Example from Germany where source block is set as WMO
        # what/source: "WMO:10103"
        # Example from The Netherlands where source block is set as a combination of ODIM and various codes
        # what/source: RAD:NL52,NOD:nlhrw,PLC:Herwijnen
        source_list = source.split(sep=",")
    wmo_code = [string for string in source_list if "WMO" in string]
    # Determine if we had exactly one WMO hit
    if len(wmo_code) == 1:
        wmo_code = wmo_code[0]
        wmo_code = wmo_code.replace("WMO:", "")
    # No wmo code found, most likeley dealing with a dutch radar
    elif len(wmo_code) == 0:
        rad_str = [string for string in source_list if "RAD" in string]
        if len(rad_str) == 1:
            rad_str = rad_str[0]
        else:
            print(
                "Something went wrong with determining the rad_str and it wasnt WMO either, exiting"
            )
            sys.exit(1)
        # Split the rad_str
        rad_str_split = rad_str.split(":")
        # [0] = RAD, [1] = rad code
        rad_code = rad_str_split[1]
        rad_codes = {"NL52": "6356", "NL51": "6234", "NL50": "6260"}
        wmo_code = rad_codes.get(rad_code)
    return int(wmo_code)


def vol2bird(
    in_file,
    out_dir,
    radar_db,
    add_version=True,
    add_sector=False,
    overwrite=False,
):
    # Construct output file
    date_regex = "([0-9]{8})"
    if add_version == True:
        version = "v0-5-0"
        suffix = pathlib.Path(in_file).suffix
        in_file_name = pathlib.Path(in_file).name
        in_file_stem = pathlib.Path(in_file_name).stem
        #
        out_file_name = in_file_stem.replace("pvol", "vp")
        out_file_name = "_".join([out_file_name, version]) + suffix
        # odim = odim_code(out_file_name)
        wmo = extract_wmo_code(in_file)
        odim = translate_wmo_odim(radar_db, wmo)
        datetime = pd.to_datetime(re.search(date_regex, out_file_name)[0])
        ibed_path = "/".join(
            [
                odim[:2],
                odim[2:],
                str(datetime.year),
                str(datetime.month).zfill(2),
                str(datetime.day).zfill(2),
            ]
        )
        # check if we need to make this dir
        out_file = "/".join([out_dir, ibed_path, out_file_name])
        out_file_dir = pathlib.Path(out_file).parent
        if not out_file_dir.exists():
            # Exists ok true because we can get race conditions
            out_file_dir.mkdir(parents=True, exist_ok=True)

    # Initialize
    process = True
    # Determine if a file exists
    if pathlib.Path(out_file).exists():
        # The file exists
        if not overwrite:
            # If we do not want to overwrite, set process to false
            process = False
            print(f"Not processing, overwrite is set to {overwrite}")
    else:
        # The file does not exist, process.
        pass

    if process:
        command = ["vol2bird", in_file, out_file]
        result = subprocess.run(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
    return [in_file, out_file]


def get_vp_storage_path(relative_path: str = "") -> str:
    return (
        pathlib.Path(param_user_email)
        .joinpath(conf_vp_output_prefix)
        .joinpath(relative_path)
    )


vertical_profile_paths = []
radar_db = load_radar_db(conf_local_radar_db)
# cast back to pathlib after deserializing
odim_pvol_paths = [pathlib.Path(path) for path in odim_pvol_paths]
futures = []
with ProcessPoolExecutor(max_workers=cpu_count) as executor:
    for odim_pvol_path in odim_pvol_paths:
        futures.append(
            executor.submit(
                vol2bird,
                in_file=odim_pvol_path,
                out_dir=conf_local_vp,
                radar_db=radar_db,
                add_version=True,
                add_sector=False,
                overwrite=False,
            )
        )
    # pvol_path, vp_path = vol2bird(
    #    odim_pvol_path, conf_local_vp, radar_db, overwrite=False
    # )
    # vertical_profile_paths.append(vp_path)
for future in futures:
    pvol_path, vp_path = future.result()
    vertical_profile_paths.append(vp_path)
print(vertical_profile_paths)
end_time_pvol_vp = time.time()
elapsed_time_pvol_vp = end_time_pvol_vp - start_time_pvol_vp
print(
    f"{param_semaphore=}\tConverting PVOL to VP: {elapsed_time_pvol_vp/60:.0f} minute(s) and {elapsed_time_pvol_vp%60:.2f} seconds"
)
io_after_pvol_vp = psutil.disk_io_counters()
io_read_mb_pvol_vp = (
    io_after_pvol_vp.read_bytes - io_before_pvol_vp.read_bytes
) / 1e6
io_write_mb_pvol_vp = (
    io_after_pvol_vp.write_bytes - io_before_pvol_vp.write_bytes
) / 1e6


start_time_clean_pvol = time.time()
if str2bool(param_clean_pvol_output):
    print("Removing PVOL output from local storage")
    for pvol_path in odim_pvol_paths:
        pathlib.Path(pvol_path).unlink()
        if not any(pathlib.Path(pvol_path).parent.iterdir()):
            pathlib.Path(pvol_path).parent.rmdir()
end_time_clean_pvol = time.time()
elapsed_time_clean_pvol = end_time_clean_pvol - start_time_clean_pvol

io_before_upload_vp = psutil.disk_io_counters()
start_time_upload_vp = time.time()
if str2bool(param_upload_results):
    # Minio version
    from minio import Minio

    minioClient = Minio(
        endpoint=conf_minio_endpoint,
        access_key=secret_minio_access_key,
        secret_key=secret_minio_secret_key,
        secure=True,
    )
    print(f"Uploading results to {get_vp_storage_path()}")
    for vp_path in vertical_profile_paths:
        vp_path = pathlib.Path(vp_path)
        local_vp_storage = pathlib.Path(conf_local_vp)
        relative_path = vp_path.relative_to(local_vp_storage)
        remote_vp_path = get_vp_storage_path(relative_path)
        # check if this exists
        exists = False
        try:
            _ = minioClient.stat_object(
                bucket=(conf_minio_user_bucket_name),
                prefix=remote_vp_path.as_posix(),
            )
            exists = True
        except:
            pass
        if not exists:
            print(f"Uploading {vp_path} to {remote_vp_path}")
            with open(vp_path, mode="rb") as file_data:
                file_stat = os.stat(vp_path)
                minioClient.put_object(
                    bucket_name=(conf_minio_user_bucket_name),
                    object_name=remote_vp_path.as_posix(),
                    data=file_data,
                    length=file_stat.st_size,
                )
        else:
            print(f"{remote_vp_path} exists, skipping ")
    print("Finished uploading results")
end_time_upload_vp = time.time()
elapsed_time_upload_vp = end_time_upload_vp - start_time_upload_vp
io_after_upload_vp = psutil.disk_io_counters()
io_read_mb_upload_vp = (
    io_after_upload_vp.read_bytes - io_before_upload_vp.read_bytes
) / 1e6
io_write_mb_upload_vp = (
    io_after_upload_vp.write_bytes - io_before_upload_vp.write_bytes
) / 1e6
start_time_clean_vp = time.time()

if str2bool(param_clean_vp_output):
    print("Removing VP output from local storage")
    for vp_path in vertical_profile_paths:
        pathlib.Path(vp_path).unlink()
        if not any(pathlib.Path(vp_path).parent.iterdir()):
            pathlib.Path(vp_path).parent.rmdir()
end_time_clean_vp = time.time()
elapsed_time_clean_vp = end_time_clean_vp - start_time_clean_vp

PVOL_VP_converter_complete = 1


# %% claude
import csv
import os
from datetime import datetime


def fmt(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}m {s:.2f}s"


def fmt_io(read_mb, write_mb):
    return f"R {read_mb:.1f} MB  W {write_mb:.1f} MB"


# ── Collect run metadata ──────────────────────────────────────────────────────
run_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

total = (
    elapsed_time_import_extra_libraries
    + elapsed_time_configuration
    + elapsed_time_secrets
    + elapsed_time_parameters
    + elapsed_time_initializing
    + elapsed_time_listknmi
    + elapsed_time_download
    + elapsed_time_knmi_convert
    + elapsed_time_pvol_upload
    + elapsed_time_pvol_vp
    + elapsed_time_clean_pvol
    + elapsed_time_upload_vp
    + elapsed_time_clean_vp
)

# ── Print to console ──────────────────────────────────────────────────────────
print(f"{'─' * 65}")
print(f"Benchmark run — {run_datetime}")
print(f"{'─' * 65}")
print(f"Start date:              {param_start_date}")
print(f"End date:                {param_end_date}")
print(f"Max KNMI files:          {param_maximum_KNMI_files}")
print(f"Interval (min):          {param_interval_in_minutes}")
print(f"Radar:                   {param_radar}")
print(f"Semaphore count:         {param_semaphore}")
print(f"User email:              {param_user_email}")
print(f"Clean KNMI input:        {param_clean_knmi_input}")
print(f"Upload results:          {param_upload_results}")
print(f"Clean PVOL output:       {param_clean_pvol_output}")
print(f"Clean VP output:         {param_clean_vp_output}")
print(f"{'─' * 65}")
print(f"{'Step':<30} {'Time':<15} {'I/O'}")
print(f"{'─' * 65}")
print(
    f"{'Import extra libraries':<30} {fmt(elapsed_time_import_extra_libraries):<15}"
)
print(f"{'Configuration':<30} {fmt(elapsed_time_configuration):<15}")
print(f"{'Secrets':<30} {fmt(elapsed_time_secrets):<15}")
print(f"{'Parameters':<30} {fmt(elapsed_time_parameters):<15}")
print(f"{'Initializing':<30} {fmt(elapsed_time_initializing):<15}")
print(f"{'List KNMI':<30} {fmt(elapsed_time_listknmi):<15}")
print(
    f"{'Download':<30} {fmt(elapsed_time_download):<15} {fmt_io(io_read_mb_download, io_write_mb_download)}"
)
print(
    f"{'KNMI convert':<30} {fmt(elapsed_time_knmi_convert):<15} {fmt_io(io_read_mb_knmi_convert, io_write_mb_knmi_convert)}"
)
print(
    f"{'PVOL upload':<30} {fmt(elapsed_time_pvol_upload):<15} {fmt_io(io_read_mb_pvol_upload, io_write_mb_pvol_upload)}"
)
print(
    f"{'PVOL VP':<30} {fmt(elapsed_time_pvol_vp):<15} {fmt_io(io_read_mb_pvol_vp, io_write_mb_pvol_vp)}"
)
print(f"{'Clean PVOL':<30} {fmt(elapsed_time_clean_pvol):<15}")
print(
    f"{'Upload VP':<30} {fmt(elapsed_time_upload_vp):<15} {fmt_io(io_read_mb_upload_vp, io_write_mb_upload_vp)}"
)
print(f"{'Clean VP':<30} {fmt(elapsed_time_clean_vp):<15}")
print(f"{'─' * 65}")
print(f"{'Total':<30} {fmt(total):<15}")

# ── CSV export ────────────────────────────────────────────────────────────────
csv_file = "benchmark_results.csv"

fieldnames = [
    "run_datetime",
    # Parameters
    "param_start_date",
    "param_end_date",
    "param_maximum_KNMI_files",
    "param_interval_in_minutes",
    "param_radar",
    "param_semaphore",
    "param_user_email",
    "param_clean_knmi_input",
    "param_upload_results",
    "param_clean_pvol_output",
    "param_clean_vp_output",
    # Timings (seconds)
    "elapsed_time_import_extra_libraries",
    "elapsed_time_configuration",
    "elapsed_time_secrets",
    "elapsed_time_parameters",
    "elapsed_time_initializing",
    "elapsed_time_listknmi",
    "elapsed_time_download",
    "elapsed_time_knmi_convert",
    "elapsed_time_pvol_upload",
    "elapsed_time_pvol_vp",
    "elapsed_time_clean_pvol",
    "elapsed_time_upload_vp",
    "elapsed_time_clean_vp",
    "elapsed_time_total",
    # I/O (MB)
    "io_read_mb_download",
    "io_write_mb_download",
    "io_read_mb_knmi_convert",
    "io_write_mb_knmi_convert",
    "io_read_mb_pvol_upload",
    "io_write_mb_pvol_upload",
    "io_read_mb_pvol_vp",
    "io_write_mb_pvol_vp",
    "io_read_mb_upload_vp",
    "io_write_mb_upload_vp",
]

row = {
    "run_datetime": run_datetime,
    # Parameters
    "param_start_date": param_start_date,
    "param_end_date": param_end_date,
    "param_maximum_KNMI_files": param_maximum_KNMI_files,
    "param_interval_in_minutes": param_interval_in_minutes,
    "param_radar": param_radar,
    "param_semaphore": param_semaphore,
    "param_user_email": param_user_email,
    "param_clean_knmi_input": param_clean_knmi_input,
    "param_upload_results": param_upload_results,
    "param_clean_pvol_output": param_clean_pvol_output,
    "param_clean_vp_output": param_clean_vp_output,
    # Timings
    "elapsed_time_import_extra_libraries": elapsed_time_import_extra_libraries,
    "elapsed_time_configuration": elapsed_time_configuration,
    "elapsed_time_secrets": elapsed_time_secrets,
    "elapsed_time_parameters": elapsed_time_parameters,
    "elapsed_time_initializing": elapsed_time_initializing,
    "elapsed_time_listknmi": elapsed_time_listknmi,
    "elapsed_time_download": elapsed_time_download,
    "elapsed_time_knmi_convert": elapsed_time_knmi_convert,
    "elapsed_time_pvol_upload": elapsed_time_pvol_upload,
    "elapsed_time_pvol_vp": elapsed_time_pvol_vp,
    "elapsed_time_clean_pvol": elapsed_time_clean_pvol,
    "elapsed_time_upload_vp": elapsed_time_upload_vp,
    "elapsed_time_clean_vp": elapsed_time_clean_vp,
    "elapsed_time_total": total,
    # I/O
    "io_read_mb_download": io_read_mb_download,
    "io_write_mb_download": io_write_mb_download,
    "io_read_mb_knmi_convert": io_read_mb_knmi_convert,
    "io_write_mb_knmi_convert": io_write_mb_knmi_convert,
    "io_read_mb_pvol_upload": io_read_mb_pvol_upload,
    "io_write_mb_pvol_upload": io_write_mb_pvol_upload,
    "io_read_mb_pvol_vp": io_read_mb_pvol_vp,
    "io_write_mb_pvol_vp": io_write_mb_pvol_vp,
    "io_read_mb_upload_vp": io_read_mb_upload_vp,
    "io_write_mb_upload_vp": io_write_mb_upload_vp,
}

file_exists = os.path.isfile(csv_file)

with open(csv_file, mode="a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    writer.writerow(row)

print(f"\nRun appended to '{csv_file}'")

# %%
