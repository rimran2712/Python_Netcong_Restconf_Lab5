from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
#from nornir_scrapli.tasks import send_command, send_configs
from nornir_netconf.plugins.tasks import netconf_get_config
import os
import ipdb
from rich import print


nr = InitNornir (config_file="/home/imran/Documents/Automation/Nornir/Runbooks_Repositories/Python_Netcong_Restconf_Lab5/Inventory/config.yaml")

# Clearing the Screen
os.system('clear')

""" 
This program will pull running config through Netconf, by default it pull all YANG models.
NETCONG provide data in XML format.
Below prohram will show all supporting YANG models, 
In future labs we will filter our output to specific YANG model
"""

def netconf_running_config (task):
    task.run (task=netconf_get_config, source="running")
    
netconf_running_config_results = nr.run (task=netconf_running_config)
print_result (netconf_running_config_results)
#ipdb.set_trace ()
