#!/usr/bin/env python3

import json
import requests
import sys
import subprocess

from Crypto.Hash import SHA256
from datetime import datetime
from xml.etree import ElementTree, ElementInclude

def git(*args):
    git_command = ['git', *args]
    subprocess.run(git_command)

def update_release_date(file_name, version, publishing_date):
    tree = ElementTree.ElementTree(file=file_name)
    root = tree.getroot()

    releases = root.find('releases')

    releases[0].attrib['version'] = version
    releases[0].attrib['date']    = publishing_date

    tree = ElementTree.ElementTree(root)

    with open(file_name, 'wb') as outfile:
        tree.write(outfile, encoding='UTF-8', xml_declaration=True)

sources = 'sources.json'
appdata = 'md.obsidian.Obsidian.appdata.xml'
metadata_url = 'https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest'

try:
    response = requests.get(metadata_url).json()
except:
    print('Could not download information on latest release. Exiting now.')
    sys.exit(1)

version = response['name']

for asset in response['assets']:
    if asset['name'] == f'obsidian-{version}.tar.gz':
        download_metadata = asset    
        break
else:
    print('Could not find release archive. Exiting now.')
    sys.exit(1)

latest_download_url = download_metadata['browser_download_url']
creation_date       = datetime.fromisoformat(download_metadata['created_at'][:-1])
publishing_date     = f'{creation_date.year}-{creation_date.month}-{creation_date.day}'

current_download_url = ''

try:
    with open(sources, 'r') as f:
        sources_data = json.loads(f.read())
        for source in sources_data:
            if source['only-arches'] == ['x86_64']:
                current_download_url = source['url']
                break
        
except:
    pass

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

# Upstream devs plan on freezing aarch64 downloads to 0.9.17 and instead use the self-update mechanism, so the aarch64
# source archive will be hardcoded
content = [{
    'type': 'archive',
    'url': latest_download_url,
    'sha256': result,
    'only-arches': ['x86_64']
}, {
    'type': 'archive',
    'url': 'https://github.com/obsidianmd/obsidian-releases/releases/download/v0.9.17/obsidian-0.9.17-arm64.tar.gz',
    'sha256': '5fe41e7b9362d6ca4c2ce6e2b8af811d8586a0ed6fcaaec715fca027bfbb7e33',
    'only-arches': ['aarch64']
}]

print(f'Placing the following data inside {sources}:')
print(json.dumps(content, sort_keys=True, indent=4))

with open(sources, 'w') as f:
    json.dump(content, f, sort_keys=True, indent=4)

update_release_date(appdata, version, publishing_date)

commit_message = f'Updating release version to {version}'

git('add', appdata, sources)
git('commit', '-m', commit_message)
