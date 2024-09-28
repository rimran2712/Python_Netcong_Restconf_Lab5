from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_http.tasks import http_method
import os
import ipdb
from rich import print
import json

nr = InitNornir (config_file="/home/imran/Documents/Automation/Nornir/Runbooks_Repositories/Python_Netcong_Restconf_Lab5/Inventory/config.yaml")

# Clearing the Screen
os.system('clear')

""" 
This program will pull router (routing protocols) configuration from running config through Restconf, 
RESTCONF provide data in either XML or Jason format. We can pick whatever we like. 
We can tell to HTTPS server that we need XML or Jason data though Request Header type "Accept" 
Below prohram will pull data in Jason format from native YANG data model 
we will get output in Jason text formated string, we will convert this Jason formated string into
Python dictionary and will store/embend into hosts inventory key to use in program
"""
'''
Below "Accept" header is request type header and in Accept header is used to 
inform the server by the client that which content type is understandable by the client.
in below exmaple client asking to server, please send him 
data in jason format from yang-data model
'''
'''
IPDB inspection of routing protocols, in our example only OSPF configured

ipdb> pp nr.inventory.hosts['CSR-R1']['routing_protocols']
{'Cisco-IOS-XE-native:router': {'Cisco-IOS-XE-ospf:router-ospf': {'ospf': {'process-id': [{'id': 127,
                                                                                           'network': [{'area': 12,
                                                                                                        'ip': '0.0.0.0',
                                                                                                        'wildcard': '0.0.0.0'}],
                                                                                           'router-id': '1.1.1.1'}]}}}}
ipdb> pp nr.inventory.hosts['CSR-R1']['routing_protocols']['Cisco-IOS-XE-native:router']['Cisco-IOS-XE-ospf:router-ospf']['ospf']
{'process-id': [{'id': 127,
                 'network': [{'area': 12,
                              'ip': '0.0.0.0',
                              'wildcard': '0.0.0.0'}],
                 'router-id': '1.1.1.1'}]}
ipdb> 

'''

http_headers = {'Accept': 'application/yang-data+json'}

def restconf_running_config (task):
    running_config = task.run (
        task=http_method, 
        method="get", 
        verify=False,
        auth=(f"{task.host.username}",f"{task.host.password}"),
        headers=http_headers,
        url=f"https://{task.host.hostname}:443/restconf/data/native/router"
        )
    task.host['routing_protocols'] = json.loads(running_config.result)
    ospf_proc_id = task.host['routing_protocols']['Cisco-IOS-XE-native:router']['Cisco-IOS-XE-ospf:router-ospf']['ospf']['process-id'][0]['id']
    print (f"[blue]{task.host}[/blue] running OSPF Process ID [red]*** {ospf_proc_id} ***[/red]")
    
nr.run (task=restconf_running_config)
#ipdb.set_trace ()
