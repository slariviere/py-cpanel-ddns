#!/usr/bin/env python

import pycpanel, yaml

# Read the cpanel hash for the connection
hashFile = open('cpanel-hash')
cpanel_hash = hashFile.read()
hashFile.close()

# Read the configuration file
configFile = open('config.yaml')
configMap = yaml.safe_load(configFile)
configFile.close()

# Connect to the server
server =  pycpanel.conn(configMap['cpanel']['hostname'], configMap['cpanel']['username'], cpanel_hash, password=None, ssl=True, verify=True, check_conn=True)

# Params for the first connection (Get the line number to edit)
params = { 'domain' : configMap['ddns']['domain'] }

dumpzone = server.api('dumpzone', params=params)

for line in dumpzone['result'][0]['record']:
    if 'name' in line:
        if line['name'] == configMap['ddns']['name']:
            break

print line


