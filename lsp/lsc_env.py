"""
Lumina NetDev Enviroment Parameters:
    Update the environment variables to match LSC deployment.
"""

# User Input

# Automation Configurable Parameters:
data_type = "json"
LSC_PARAMS = {
    "host": "http://192.168.86.243:8181",
    "username": "admin",
    "password": "admin",
    "type": data_type,
    "contenttype": "application/" + data_type,
    "accept": "application/" + data_type,
    "addlsptplt": "/opt/lumina/lsc-automation-scripts/lsp/templates/add_lsp." + data_type,
    "updatelsptplt": "/opt/lumina/lsc-automation-scripts/lsp/templates/update_lsp." + data_type,
    "removelsptplt": "/opt/lumina/lsc-automation-scripts/lsp/templates/remove_lsp." + data_type,
    "lspinputfile": "/opt/lumina/lsc-automation-scripts/lsp/data/lsps.csv"
}

# End User Input
