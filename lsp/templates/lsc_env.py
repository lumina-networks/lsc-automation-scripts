"""
Lumina NetDev Environment Parameters:
    Update the environment variables to match LSC deployment.
"""

# User Input

data_type = "json" #Valid Values=(json,xml)
LSC_PARAMS = {
    "host": "http://localhost:8181",
    "username": 'admin',
    "password": 'admin',
    "type": data_type,
    "contenttype": "application/" + data_type,
    "accept": "application/" + data_type,
    "addlsptplt": "templates/add_lsp." + data_type,
    "updatelsptplt": "templates/update_lsp." + data_type,
    "removelsptplt": "templates/remove_lsp." + data_type,
    "lspinputfile": "data/lsps.csv"
}

# End User Input
