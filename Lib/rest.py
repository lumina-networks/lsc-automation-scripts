#!/usr/bin/env python

"""
Lumina NetDev Automation Library Script:
    This library provides a set of utilities based on 'requests' to  
    interact with REST APIs, format body messages from templates,
    etc...
"""

import requests
import base64


###############################################################################

def invoke_rest(uri, method, body, user, passwd, dataType="json", timeout=5):
    """
    Invoke arbitrary REST call and returns response object
    
    Parameters
    ----------
    uri : str
        URI to call
    method : {'GET', 'POST', 'PUT', 'DELETE'}
        HTTP Method Type
    body : dict
        HTTP request body
    user : str
        Authentication user name
    passwd : str
        Authentication user password
    dataType : {'json', 'xml'}, optional
        HTTP body format. Defaults to ``json``
    timeout : int, optional
        Rest call timeout in seconds. Defaults to ``5``
    
    Returns
    -------
    response : requests.Response object or None
        Response object from Python requests
    
    Raises
    ------
    None
        If exception occurs, ``None``
    
    Examples
    --------
    >>> import rest
    >>> req = rest.invoke_rest('http://localhost:8181/restconf/operational/network-topology:network-topology/', 'GET', '', 'admin', 'password')
    [REST] GET http://localhost:8181/restconf/operational/network-topology:network-topology/
    >>> req
    <Response [200]>
    
    >>> req = rest.invoke_rest('/restconf/', 'GET', '', 'admin', 'password')
    [REST] GET /restconf/
    >>> req
    None
    """
    print ('INFO:::[REST] %s %s\n%s' % (method, uri, body))
    try:
        if dataType == "xml":
            #print "DEBUG:::Attempting an XML request for uri={0}".format(uri)
            return requests.request(method=method, url=uri, headers={
                'Content-Type': "application/" + dataType,
                'Accept': "application/" + dataType,
                'Authorization': 'Basic ' + base64.b64encode('%s:%s' % (user, passwd))
            }, data=body, timeout=timeout)
        else:
            #print "DEBUG:::Attempting a JSON request for uri={0}".format(uri)
            return requests.request(method=method, url=uri, headers={
                'Content-Type': "application/" + dataType,
                'Accept': "application/" + dataType,
                'Authorization': 'Basic ' + base64.b64encode('%s:%s' % (user, passwd))
            }, data=body, timeout=timeout)
    except Exception:
        return None


###############################################################################
