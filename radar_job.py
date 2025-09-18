import requests
import subprocess
import os

# NOAA MRMS radar file URL (latest composite reflectivity)
url = 'https://mrms.ncep.noaa.gov/data/2D/MergedReflectivityQCComposite/latest.grib2.gz'
download_path = '/tmp/latest.grib2.gz'
unzipped_path = '/tmp/latest.grib2'
warped_path = '/tmp/latest_3857.tif'
png_path = '/render/public/latest.png'  # Render serves files from /render/public

# Download radar file
print("Downloading radar data...")
r = requests.get(url)
with open(download_path, 'wb') as f:
    f.write(r.content)

# Unzip the file
print("Unzipping radar file...")
subprocess.run(['gunzip', '-f', download_path])

# Reproject to Web Mercator
print("Reprojecting to EPSG:3857...")
subprocess.run([
    'gdalwarp',
    '-t_srs', 'EPSG:3857',
    unzipped_path,
    warped_path
])

# Colorize using a custom ramp (you’ll create this file next)
print("Applying color ramp...")
subprocess.run([
    'gdaldem',
    'color-relief',
    warped_path,
    'viper-ramp.txt',
    png_path,
    '-alpha'
])

print("Radar image saved to:", png_path)