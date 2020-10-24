#!/usr/bin/env python3

# This script serves to work around an issue with folder deletion not behaving properly
# when attempting to use the system trash

import os
import sys
import json

trash_behavior = 'local'

try:
    obsidian_config_home = os.environ['XDG_CONFIG_HOME']
    obsidian_config = f'{obsidian_config_home}/obsidian/obsidian.json'

    with open(obsidian_config, 'r') as f:
        obsidian_data = json.loads(f.read())

    vaults = obsidian_data['vaults']
except:
    print('Could not get Obsidian config. Skipping trash behavior update.')
    sys.exit(0)

# Obsidian doesn't have a global trash preference, each vault has to be checked. This also means
# trash behavior has to be set for each new vault upon creation, or have Obsidian restart
for vault, vault_config in vaults.items():
    try:
        vault_path = vault_config['path']
        vault_config = f'{vault_path}/.obsidian/config'

        with open(vault_config, 'r') as f:
            vault_data = json.loads(f.read())

        if not 'trashOption' in vault_data or vault_data['trashOption'] == 'system':
            vault_data['trashOption'] = trash_behavior

        with open(vault_config, 'w') as outfile:
            json.dump(vault_data, outfile, indent=2)

    except:
        print(f'Could not open/update vault \'{vault}\'')

