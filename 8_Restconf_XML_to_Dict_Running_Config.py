from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_http.tasks import http_method
import os
import ipdb
from rich import print
import xmltodict

nr = InitNornir (config_file="/home/imran/Documents/Automation/Nornir/Runbooks_Repositories/Python_Netcong_Restconf_Lab5/Inventory/config.yaml")

# Clearing the Screen
os.system('clear')

""" 
This program will pull router (routing protocols) configuration from running config through Restconf, 
RESTCONF provide data in either XML or Jason format. We can pick whatever we like. 
We can tell to HTTPS server that we need XML or Jason data though Request Header type "Accept" 
Below prohram will pull data in Jason format from native YANG data model 
"""
'''
Below "Accept" header is request type header and in Accept header is used to 
inform the server by the client that which content type is understandable by the client.
in below exmaple client asking to server, please send him data in xml format from yang-data model
'''

'''
IPDB inspection of routing protocols, in our example only OSPF configured

ipdb> pp nr.inventory.hosts['CSR-R1']['routing_protocols']['router']
{'@xmlns': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native',
 '@xmlns:ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native',
 'router-ospf': {'@xmlns': 'http://cisco.com/ns/yang/Cisco-IOS-XE-ospf',
                 'ospf': {'process-id': {'id': '127',
                                         'network': {'area': '12',
                                                     'ip': '0.0.0.0',
                                                     'wildcard': '0.0.0.0'},
                                         'router-id': '1.1.1.1'}}}}
ipdb> 

'''


http_headers = {'Accept': 'application/yang-data+xml'}

def restconf_running_config (task):
    running_config = task.run (
        task=http_method, 
        method="get", 
        verify=False,
        auth=(f"{task.host.username}",f"{task.host.password}"),
        headers=http_headers,
        url=f"https://{task.host.hostname}:443/restconf/data/native/router"
        )
    task.host['routing_protocols'] = xmltodict.parse(running_config.result)
    ospf_proc_id = task.host['routing_protocols']['router']['router-ospf']['ospf']['process-id']['id']
    print (f"[blue]{task.host}[/blue] running OSPF Process ID [red]*** {ospf_proc_id} ***[/red]")
   
nr.run (task=restconf_running_config)
#ipdb.set_trace ()
