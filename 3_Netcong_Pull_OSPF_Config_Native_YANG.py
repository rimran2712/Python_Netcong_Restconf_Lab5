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
This program will pull OSPF configuration from running config through Netconf, 
We will filter output to Native YANG model using xpath & filters options
NETCONG provide data in XML format.
Below prohram will only data modeled in native YANG model 
We can filter upto any tag in XML data
"""

def netconf_running_config (task):
    running_config = task.run (task=netconf_get_config, 
                               source="running", 
                               path="/native/router/router-ospf/ospf", 
                               filter_type="xpath")
    
netconf_running_config_results = nr.run (task=netconf_running_config)
print_result (netconf_running_config_results)
#ipdb.set_trace ()
