#!/usr/bin/env python3

import json
import requests
import sys
from Crypto.Hash import SHA256
# https://pypi.org/project/python-dateutil/
import dateutil.parser

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


posts = requests.get('https://forum.obsidian.md/c/announcements/13.json').json()

formatted_version = f"obsidian-release-v{version.replace('.','-')}"

for post in posts['topic_list']['topics']:
    if post['slug'] == formatted_version:
        post_date = dateutil.parser.parse(post['created_at'])
        break

