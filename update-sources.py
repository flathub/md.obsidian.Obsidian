#!/usr/bin/env python3

import json
import requests
import sys
from Crypto.Hash import SHA256
# https://pypi.org/project/python-dateutil/
import dateutil.parser

sources = 'sources.json'
metadata_url = 'https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest'

try:
    response = requests.get(metadata_url).json()

    version = response['name']

    latest_download_url = f'https://github.com/obsidianmd/obsidian-releases/releases/download/v{version}/obsidian-{version}.tar.gz'

except:
    print('Could not download information on latest release. Exiting now.')
    sys.exit(1)

try:
    with open(sources, 'r') as f:
        current_download_url = json.loads(f.read())['url']

except:
    current_download_url = ''

if latest_download_url == current_download_url:
    print(f'No new release. Current release is still {version}')
    sys.exit(0)

print(f'Downloading file from {latest_download_url}')

downloaded_file = requests.get(latest_download_url)

if downloaded_file.status_code != 200:
    print(f'Error: File not found!')
    sys.exit(1)

release_archive = downloaded_file.content

checksum = SHA256.new()

checksum.update(release_archive)
result = checksum.hexdigest()

content = {
    'type': 'archive',
    'url': latest_download_url,
    'sha256': result
}

print(f'Placing the following data inside {sources}:')
print(json.dumps(content, sort_keys=True, indent=4))

with open(sources, 'w') as f:
    json.dump(content, f, sort_keys=True, indent=4)
