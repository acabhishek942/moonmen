# moonmen
Synchronised folder across multiple devices

# Usage 
moonmen can be used with two commands ``server`` and ``client``
## server
``python3 moonmen/start.py server -p 8124 -d /Users/ac/Moonmen/MoonmenServer -b ./.moonmen-server-backup``

## client 
``python3 moonmen/start.py client -o 192.168.43.201 -p 8124 -d /Users/ac/Moonmen/MoonmenClient -b ./.moonmen-client-bckup``

# Help
use ``python3 moonmen/start.py (server|client) --help`` to see all the arguments that can be passed
