import json
import os
import ipaddress


#### Variables
# Name for address list in Mikrotik
list_name = "blocked-ips"
# Source file name
source_filename = "rkn.json"

########################################################################################################################
respath = os.path.normpath(os.path.dirname(__file__) + '/resources')
if not os.path.exists(source_filename):
    source_filename = os.path.normpath(os.path.dirname(__file__) + '/' + source_filename)

rkn_json_path = os.path.normpath(source_filename)

try:
    os.mkdir(respath)
except FileExistsError:
    pass

with open(rkn_json_path, 'r', encoding="utf8") as fp:
    json_parsed = json.load(fp)

with open(respath + '/ipv4.txt', 'w', encoding="utf8") as fp:
    fp.write('/ip firewall address-list\n')
    for ip in json_parsed:
        try:
            ip_addr = ipaddress.ip_address(ip)
        except ValueError as e:
            ip_addr = ipaddress.ip_network(ip)
        except:
            pass

        if isinstance(ip_addr, ipaddress.IPv4Address) or isinstance(ip_addr, ipaddress.IPv4Network):
            fp.write("add address=" + ip + " list={0}\n".format(list_name))
