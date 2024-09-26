from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
#from nornir_scrapli.tasks import send_command, send_configs
from nornir_netconf.plugins.tasks import netconf_get_config
import os
import ipdb
from rich import print
import xmltodict

nr = InitNornir (config_file="/home/imran/Documents/Automation/Nornir/Runbooks_Repositories/Python_Netcong_Restconf_Lab5/Inventory/config.yaml")

# Clearing the Screen
os.system('clear')

""" 
This program will pull running config through Netconf, 
We will filter output to Native YANG model using xpath & filters options
NETCONG provide data in XML format.
Below prohram will only data modeled in native YANG model 
NETCONF provide data in XML format, We can convert this XML data into Python dictionary and
store/embend in host inventory file like below, we will also inspect host key with ipdb

Assumtion: Please make sure you are running basic OSFP on devices because code will pull OSPF Process ID
"""
"""
IPDB inspection of routing protocols, in our example only OSPF configured

ipdb> pp nr.inventory.hosts['CSR-R1']['run_cfg']
{'data': {'@xmlns': 'urn:ietf:params:xml:ns:netconf:base:1.0',
          '@xmlns:nc': 'urn:ietf:params:xml:ns:netconf:base:1.0',
          'native': {'@xmlns': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native',
                     'router': {'ospf': {'@xmlns': 'http://cisco.com/ns/yang/Cisco-IOS-XE-ospf',
                                         'auto-cost': {'reference-bandwidth': '100'},
                                         'compatible': {'rfc1583': None},
                                         'id': '127',
                                         'timers': {'throttle': {'spf': {'delay': '50',
                                                                         'max-delay': '5000',
                                                                         'min-delay': '200'}}}},
                                'router-ospf': {'@xmlns': 'http://cisco.com/ns/yang/Cisco-IOS-XE-ospf',
                                                'ospf': {'process-id': {'id': '127',
                                                                        'network': {'area': '12',
                                                                                    'ip': '0.0.0.0',
                                                                                    'wildcard': '255.255.255.255'}}}}}}}}
ipdb> 

"""
def netconf_running_config (task):
    running_config = task.run (task=netconf_get_config, 
                               source="running", 
                               path="/native/router", 
                               filter_type="xpath")
    task.host['run_cfg'] = xmltodict.parse(running_config.result.rpc.data_xml)
    ospf_proc_id = task.host['run_cfg']['data']['native']['router']['ospf']['id']
    print (f"[blue]{task.host}[/blue] running OSPF Process ID [red]*** {ospf_proc_id} ***[/red]")
        
nr.run (task=netconf_running_config)

#ipdb.set_trace ()

