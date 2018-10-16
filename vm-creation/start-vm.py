# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys
from os import environ as env

from novaclient.client import Client
from neutronclient.v2_0 import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "ACCHT18.normal" 
private_net = "SNIC 2018/10-30 Internal IPv4 Network"
floating_ip_pool_name = "Public External IPv4 network"
floating_ip = None
image_name = "Ubuntu 16.04 LTS (Xenial Xerus) - latest"
key = "2svni7746"

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
    print nova_client
    print net
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
    instance = nova_client.servers.create(name="vm1", image=image, flavor=flavor, userdata=userdata, nics=nics, security_groups=secgroups)
    inst_status = instance.status
    print "waiting for 10 seconds.. "
    time.sleep(10)
    
    while inst_status == 'BUILD':
        print "Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more..."
        time.sleep(5)
        instance = nova_client.servers.get(instance.id)
        inst_status = instance.status
        
        print "Instance: "+ instance.name +" is in " + inst_status + "state"
