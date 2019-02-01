#!/usr/bin/env python

"""
Lumina NetDev Automation Script:
    Provides a quick way to add, update, and remove LSPs using PCEP.
    Users should update the env.py environment variables prior to
    running this script.
"""

import requests
import lsc_env
import csv
import json
import base64
import dpath
from StdSuites.Table_Suite import row
# https://github.com/akesterson/dpath-python


# Module Vars:
lspAdd = "/restconf/operations/network-topology-pcep:add-lsp"
lspUpdate = "/restconf/operations/network-topology-pcep:update-lsp"
lspRemove = "/restconf/operations/network-topology-pcep:remove-lsp"
lspOperation = ""
uri = ""
postMestod = "POST"
getMethod = "GET"
timeout = 2


###############################################################################

def invoke_rest(uri, method, body, timeout=5):
    """
    Invoke arbitrary REST call and return result
    :param uri:  URI to call
    :param method: HTTP method
    :param body: HTTP body
    :param timeout: Rest call timeout in seconds. Defaults to 5
    :return: API call output
    """
    print ('[REST] %s %s\n%s' % (method, uri, body))
    try:
        return requests.request(method=method, url=uri, headers={
            'Content-Type': lsc_env.LSC_PARAMS['contenttype'],
            'Accept': lsc_env.LSC_PARAMS['accept'],
            'Authorization': 'Basic ' + base64.b64encode('%s:%s' % (lsc_env.LSC_PARAMS['username'], lsc_env.LSC_PARAMS['password']))
        }, data=body, timeout=timeout).json()
    except Exception:
        return None

###############################################################################

def parse_csv(file):
    """
    Parse the input csv file into a python data dictionary.
    :param file:  Full file path, name and extension - ex /opt/app/script/input_data.csv
    :return: Data dictionary array of the input file with first row used as key names
    """
    # Open the CSV, read the data (first row should contain the headers)
    # The first row will be skipped and used as the key names
    data = csv.DictReader(open(file, 'r'))
    
    # Parse the CSV into a Dictionary to return
    ret = []
    for row in data:
        ret.append(row)
    
    # Parse the CSV into JSON
    #ret = json.dumps( [ row for row in data_in ] )
    
    print "DEBUG:::Returning data set=" + ret
    return ret

###############################################################################

def make_body(templateFile, userData, type="json"):
    """
    Parse the input csv file into a Python data dictionary.
    :param templateFile:  Full file path, name and extension - ex /opt/app/script/add_lsp.json
    :param userData: The dictionary of data to substitute into the template data
    :param type: The return data format json or xml.
    :return: JSON request body/payload
    """
    # Get the template file based on type:
    if type == "json":
        ret = json.loads(open(templateFile, 'r'))
    elif type == "xml":
        # @TODO add support for getting the xml template file.
        print ("")
    else:
        print ("ERROR:::Only JSON or XML type supported!  Unsupported type=" + type + "\n")
        return None
    
    # Iterate over the template and substitute user data values
    # Template contains key value pairs in xml or json format where:
    #    key --> matches YANG model
    #    value --> matches PostMan variable sub format {{var_name}}
    for row in ret:
        print ("DEBUG:::Current row=" + row + "\n")
        # @TODO need a regex to look for {{var_name}}
        
    
    # Return the body:
    return ret

###############################################################################



if lspOperation == "add":
    uri = lsc_env.LSC_PARAMS['host'] + lspAdd
    userData = parse_csv(lsc_env.LSC_PARAMS['lspinputfile'])
    body = make_body(lsc_env.LSC_PARAMS['addlsptplt'], userData, lsc_env.LSC_PARAMS['type'])
    invoke_rest(uri, postMethod, body, timeout)
elif lspOperation == "update":
    uri = lsc_env.LSC_PARAMS['host'] + lspUpdate
    invoke_rest(uri, postMethod, body, timeout)
elif lspOperation == "remove":
    uri = lsc_env.LSC_PARAMS['host'] + lspRemove
    invoke_rest(uri, postMethod, body, timeout)
else:
    print ("ERROR: Invalid LSP Operation=" + lspOperation)
    exit

invoke_rest(uri, postMethod, body)
