# LSP Project
This project provides a way to manage LSPs using the LSC PCEP API calls to add,
update and remove LSPS.  The manage\_lsps.py script uses the lsc\_env.py variables
to connect to the controller, specify REST payload body format, etc...  The user
csv data file(s) should be placed in the data directory.

The template files provide either json or xml payload formats and use
{{variable_name}} PostMan variable syntax for replacement values.  This allows for
testing and usage of the template file in PostMan with minimal effort.  The
variable names must match the column headers in the data csv file.

## Example:
Data file:  lsps.csv

```
"index","operation","lsp-name","new-variable"
1,"add","Test-lsp-1","new_value"
```

Template File: add\_lsp.json

```
{
  "network-topology-pcep:input": {
    "network-topology-pcep:name": "{{lsp-name}}",
    "network-topology-pcep:node": "pcc://{{new-variable}}",
  }
}
```

Payload/Body will become this:

```
{
  "network-topology-pcep:input": {
    "network-topology-pcep:name": "Test-lsp-1",
    "network-topology-pcep:node": "pcc://new_value",
  }
}
```

## Prerequisites
1. The LSC must be configured as the following:
    - BGP-LS neighbor to one or more BGP speakers.
    - As a PCE for all PCC routers where LSPs will be managed.
1. Python + libraries

## Installation & Configuration:
1. Requires Python env and the additional libraries to run the scripts.
    - Install instructions may be found here:  <https://docs.python-guide.org/starting/installation/>
    - `pip install xmltodict`
    - `pip install re`
    - `pip install requests`
    - `pip install dpath`
1. Project found here:  <https://github.com/lumina-networks/lsc-automation-scripts>

```sh
mkdir -p /opt/lumina/
git clone https://github.com/lumina-networks/lsc-automation-scripts.git

cd lsc-automation-scripts/lsp

# Set up a local copy of lsc_env.py
cp templates/lsc_env.py .
# Edit the lsc_env.py file variables to match your env
vi lsc_env.py

# Review/Edit the files in the data & templates directories.
ls templates/ #Contains template files
ls data/ #Contains example lsp input files

# Set up a local user data lsp file:
# NOTE: The file name may be changed, just ensure it matches the name in your lsc_env.py
cp data/lsps_single.csv data/lsps.csv
# Edit the data file for 1 or more lsp operations to perform
vi lsps.csv
```

## Executing:


```sh
cd /opt/lumina/lsc-automation-scripts/lsp
python manage_lsps.py
```
