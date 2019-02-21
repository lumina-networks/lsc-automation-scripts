# lsc-automation-scripts
Scripts to automate common Lumina SDN Controller use cases.

# Projects:

## LSP
This project provides a way to manage LSPs using the LSC PCEP API calls to add, update and remove LSPS.
The LSC must be configured as the following:
  - BGP-LS neighbor to one or more BGP speakers.
  - As a PCE for all PCC routers where LSPs will be managed.
