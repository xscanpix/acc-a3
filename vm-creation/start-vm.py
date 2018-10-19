# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html

# python-openstackclient version 3.11.0

import time, os, sys
from os import environ as env

from novaclient.client import Client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "ACCHT18.normal" 
private_net = "SNIC 2018/10-30 Internal IPv4 Network"
floating_ip_pool_name = "Public External IPv4 network"
floating_ip = None
image_name = "Ubuntu 16.04 LTS (Xenial Xerus) - latest"
key = "2svni7746"
instance_name = "svni7746-important"

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova_client = Client('2.1', session=sess)
print "user authorization completed."

image = nova_client.glance.find_image(image_name)
flavor = nova_client.flavors.find(name=flavor)

if private_net != None:
    net = nova_client.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/cloud-config.yml'
if os.path.isfile(cfg_file_path):
    userdata = open(cfg_file_path)
else:
    sys.exit("cloud-cfg.txt is not in current working directory")

secgroups = ['default']

if True:
    print "Creating instance ... "
    instance = nova_client.servers.create(name=instance_name, image=image, flavor=flavor, userdata=userdata, nics=nics, security_groups=secgroups, key_name=key)
    inst_status = instance.status
    print "waiting for 10 seconds.. "
    time.sleep(10)
    
    while inst_status == 'BUILD':
        print "Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more..."
        time.sleep(5)
        instance = nova_client.servers.get(instance.id)
        inst_status = instance.status
        
        print "Instance: "+ instance.name +" is in " + inst_status + "state"


floating_ips = nova_client.floating_ips.list()
free_floating_ips = []

for ip in floating_ips:
    if ip.instance_id == None:
        free_floating_ips.append(ip)

instance.add_floating_ip(free_floating_ips[0])

env['vm-ip'] = str(free_floating_ips[0].ip)
print(str(free_floating_ips[0].ip))
