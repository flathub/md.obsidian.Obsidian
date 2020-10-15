#!/usr/bin/env python3

import json
import requests
import sys
from Crypto.Hash import SHA256

url = 'https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/desktop-releases.json'
destination = 'sources.json'

response = requests.get(url).json()

version = response['latestVersion']

download_version = f'https://github.com/obsidianmd/obsidian-releases/releases/download/v{version}/obsidian-{version}.tar.gz'

print(f'Downloading file from {download_version}')

downloaded_file = requests.get(download_version)

if downloaded_file.status_code != 200:
    print(f'Error: File not found!')
    sys.exit(1)

release_archive = downloaded_file.content

checksum = SHA256.new()

checksum.update(release_archive)
result = checksum.hexdigest()

content = {
    'type': 'archive',
    'url': download_version,
    'sha256': result
}

print(f'Placing the following data inside {destination}:')
print(json.dumps(content, sort_keys=True, indent=4))

with open(destination, 'w') as f:
    json.dump(content, f, sort_keys=True, indent=4)
