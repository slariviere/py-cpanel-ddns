#!/usr/bin/env python

import pycpanel, yaml, urllib2

# Read the cpanel hash for the connection
hashFile = open('cpanel-hash')
cpanel_hash = hashFile.read()
hashFile.close()

# Read the configuration file
configFile = open('config.yaml')
configMap = yaml.safe_load(configFile)
configFile.close()

# Connect to the server
print "[+] Connecting to cpanel server (" + configMap['cpanel']['hostname'] + ")"
server =  pycpanel.conn(configMap['cpanel']['hostname'], configMap['cpanel']['username'], cpanel_hash, password=None, ssl=True, verify=True, check_conn=True)

# Params for the first connection (Get the line number to edit)
params = { 'domain' : configMap['ddns']['domain'] }

dumpzone = server.api('dumpzone', params=params)

found = False
for line in dumpzone['result'][0]['record']:
    if 'name' in line:
        if line['name'] == configMap['ddns']['name']:
            found = True
            break

if not found:
    print "Requested record not found"
    exit(1)

# Get the WAN ip address
p = urllib2.urlopen(configMap['ip']['url'])
ip = p.read();

# Prepare the edit parameter
editParams = {
        'domain': configMap['ddns']['domain'],
        'line': line['Line'],
        'address': ip,
        'type': 'A'
}


editzone = server.api('editzonerecord', params=editParams)

if "Bind reloading on" in  editzone['result'][0]['statusmsg']:
    print "[+] Update successful:" + editzone['result'][0]['statusmsg']
