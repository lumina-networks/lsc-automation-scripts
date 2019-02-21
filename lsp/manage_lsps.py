#!/usr/bin/env python

"""
Lumina NetDev Automation Script:
    Provides a quick way to add, update, and remove LSPs using PCEP.
    Users should update the env.py environment variables prior to
    running this script.
"""

import sys
sys.path.append('../Lib')
import rest
import lsc_env
import csv
import json
import xmltodict
import re
import dpath
from StdSuites.Table_Suite import row
# https://github.com/akesterson/dpath-python


# Module Vars:
lspAdd = "/restconf/operations/network-topology-pcep:add-lsp"
lspUpdate = "/restconf/operations/network-topology-pcep:update-lsp"
lspRemove = "/restconf/operations/network-topology-pcep:remove-lsp"
getBgpTopology = "/restconf/operational/network-topology:network-topology/"
lspOperation = ""
uri = ""
method = ""
postMethod = "POST"
getMethod = "GET"
deleteMethod = "DELETE"
timeout = 2


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
        
    #print "DEBUG:::Returning data set={}".format(ret)
    return ret


###############################################################################

def make_body(templateFile, userData, type="json"):
    """
    Parse the input csv file into a Python data dictionary.
    
    Parameters
    ----------
    templateFile : str
        Full file path, name and extension - ex templates/add_lsp.json
    userData : dict
        The dictionary of user data for substitution into the template file data
    type : {'json', 'xml'}, optional
        The templateFile data format json or xml. Defaults to ``json``

    Returns
    -------
    tpltDataStr : dict
        Request body/payload as Dictionary
    
    Examples
    --------
    >>> row = {'index': '1', 'hold-priority': '2', 'ero-hops': '10.1.2.1/32|10.2.3.1/32', 'source-ipv4-address': '1.1.1.1', 'lsp-name': 'Test-lsp-1', 'setup-priority': '0', 'operation': 'add', 'destination-ipv4-address': '3.3.3.3', 'node-id': '192.168.1.245'}
    >>> body = make_body('templates/add_lsp.xml', row, lsc_env.LSC_PARAMS['type'])
    >>> body
    {"network-topology-pcep:input": {"network-topology-pcep:arguments": {"network-topology-pcep:lspa": {"network-topology-pcep:setup-priority": "0", "network-topology-pcep:processing-rule": "false", "network-topology-pcep:ignore": "false", "network-topology-pcep:hold-priority": "2"}, "network-topology-pcep:ero": {"network-topology-pcep:processing-rule": "false", "network-topology-pcep:ignore": "false", "network-topology-pcep:subobject": [{"ip-prefix": {"network-topology-pcep:ip-prefix": "10.1.2.1/32"}, "network-topology-pcep:loose": "false"},{"ip-prefix": {"network-topology-pcep:ip-prefix": "10.2.3.1/32"}, "network-topology-pcep:loose": "false"}]}, "network-topology-pcep:bandwidth": {"network-topology-pcep:processing-rule": "false", "network-topology-pcep:ignore": "false", "network-topology-pcep:bandwidth": "SZiWgA=="}, "network-topology-pcep:odl-pcep-ietf-stateful07:lsp": {"network-topology-pcep:odl-pcep-ietf-stateful07:delegate": "true", "network-topology-pcep:odl-pcep-ietf-stateful07:administrative": "true", "network-topology-pcep:odl-pcep-ietf-stateful07:processing-rule": "false", "network-topology-pcep:odl-pcep-ietf-stateful07:ignore": "false", "network-topology-pcep:odl-pcep-ietf-stateful07:operational": "up"}, "network-topology-pcep:endpoints-obj": {"network-topology-pcep:processing-rule": "false", "network-topology-pcep:ignore": "false", "ipv4": {"network-topology-pcep:destination-ipv4-address": "3.3.3.3", "network-topology-pcep:source-ipv4-address": "1.1.1.1"}}}, "network-topology-pcep:network-topology-ref": "/network-topology:network-topology/network-topology:topology[network-topology:topology-id='pcep-topology']", "network-topology-pcep:name": "Test-lsp-1", "network-topology-pcep:node": "pcc://192.168.1.245"}}
    """
    # Get the template file based on type:
    if type == "json":
        tpltData = json.load(open(templateFile, 'r'))
        #print "DEBUG:::templateFile data={0}".format(tpltData)
    elif type == "xml":
        # @TODO add support for getting the xml template file.
        tpltData = xmltodict.parse(open(templateFile, 'r'))
        #print "DEBUG:::XML templateFile data={0}".format(tpltData)
    else:
        print ("ERROR:::Only JSON or XML type supported!  Unsupported type=" + type + "\n")
        return None
    
    # Iterate over the template and substitute user data values
    # Template contains key value pairs in xml or json format where:
    #    key --> matches YANG model
    #    value --> matches PostMan variable sub format {{var_name}}
    tpltDataStr = json.dumps(tpltData)
    #print "DEBUG:::Before Subs tpltDataStr={0}".format(tpltDataStr)
    
    for uKey,uVal in userData.items():
        #print "DEBUG:::key={0} value={1}".format(uKey,uVal)
        pattern = re.compile('{{' + uKey + '}}')
        #print "DEBUG:::regex match={0}".format(pattern.search(tpltDataStr))
        
        if uKey == "ero-hops":
            #Special Case for Ero Hops - the replacement string is type dependent
            # NOTE: The xml does not import with necessary array brackets, so
            #       handling this with the pre/post Char values.
            if type == 'xml':
                replaceStr = '{"loose": "false", "ip-prefix": {"ip-prefix": "{{ero-hops}}"}}'
                preChar = "["
                postChar = "]"
            else:
                replaceStr = '{"ip-prefix": {"network-topology-pcep:ip-prefix": "{{ero-hops}}"}, "network-topology-pcep:loose": "false"}'
                preChar = ""
                postChar = ""
            
            # Generate the appropriate number of json subobjects and set each
            # route hop ip address.
            eroHops = uVal.split("|")
            subObject = preChar
            for eroHop in eroHops:
                # Generate the appropriate number of subobjects and set each
                # route hop ip address.
                if subObject != preChar:
                    subObject += ","
                subObject += replaceStr
                subObject = re.sub(pattern, eroHop, subObject)
                #print "DEBUG:::Current subObject={0}".format(subObject)
            
            # Append the postChar
            subObject += postChar
            
            # Now replace the original template subobject with full ERO
            pattern = re.compile(replaceStr)
            #pattern.replace("{", "\{").replace("}", "\}")
            #print "DEBUG:::pattern={0}".format(pattern)
            tpltDataStr = pattern.sub(subObject, tpltDataStr)
        else:
            # Use regex to look for {{var_name}}
            #print "DEBUG:::regex match={0}".format(pattern.search(tpltDataStr))
            if pattern.search(tpltDataStr) != None:
                tpltDataStr = pattern.sub(uVal, tpltDataStr)
    
    #print "DEBUG:::After Subs templateJsonStr={0}".format(tpltDataStr)
    
    # Return the body:
    if type == "xml":
        tpltDataStr = xmltodict.unparse(json.loads(tpltDataStr), pretty=True)

    #print "DEBUG:::Return={0}".format(tpltDataStr)
    return tpltDataStr


###############################################################################

def manage_lsps():
    inputData = parse_csv(lsc_env.LSC_PARAMS['lspinputfile'])
    for i, row in enumerate(inputData):
        #print "DEBUG:::Row number={0} and data={1}".format(i,row)
        lspOperation = row['operation']
    
        if lspOperation == "add":
            method = postMethod
            uri = lsc_env.LSC_PARAMS['host'] + lspAdd
            body = make_body(lsc_env.LSC_PARAMS['addlsptplt'], row, lsc_env.LSC_PARAMS['type'])
        elif lspOperation == "update":
            method = postMethod
            uri = lsc_env.LSC_PARAMS['host'] + lspUpdate
            body = make_body(lsc_env.LSC_PARAMS['updatelsptplt'], row, lsc_env.LSC_PARAMS['type'])
        elif lspOperation == "remove":
            method = postMethod
            uri = lsc_env.LSC_PARAMS['host'] + lspRemove
            body = make_body(lsc_env.LSC_PARAMS['removelsptplt'], row, lsc_env.LSC_PARAMS['type'])
        else:
            print "ERROR: Invalid LSP Operation={0} on row={1}".format(lspOperation,row)
            exit
        
        #print "DEBUG:::URI={0}; method={1}; body={2}".format(uri, method, body)
        request = rest.invoke_rest(uri, method, body, lsc_env.LSC_PARAMS['username'], lsc_env.LSC_PARAMS['password'], lsc_env.LSC_PARAMS['type'], timeout)
        print "INFO:::Status Code={0}".format(request.status_code)
        #print "DEBUG:::Text request={0}".format(request.text)
        #print "DEBUG:::Content request={0}".format(request.content)
        
        if (request != None):
            #if ('status_code' in request and request.status_code < 300):
            if (request.status_code < 300):
                print "INFO:::SUCCESS - Response content={0}".format(request.content)
            else:
                print "ERROR:::request={0}".format(request.content)
        else:
            print "ERROR:::Unknown error encountered for method={0}, uri={1}".format(method, uri)

###############################################################################

if __name__ == "__main__":
    manage_lsps()

# SOME TESTS:
#Get the bgp topology
#uri = lsc_env.LSC_PARAMS['host'] + getBgpTopology
#request = rest.invoke_rest(uri, getMethod, '', lsc_env.LSC_PARAMS['username'], lsc_env.LSC_PARAMS['password'], lsc_env.LSC_PARAMS['type'], timeout)
#print "DEBUG:::BGP Topology request={0}".format(request.content)

# TEST BAD URI REQUEST
#uri = "/restconf/"
#request = rest.invoke_rest(uri, getMethod, '', lsc_env.LSC_PARAMS['username'], lsc_env.LSC_PARAMS['password'])
#print "DEBUG:::TEST request={0}".format(request)

