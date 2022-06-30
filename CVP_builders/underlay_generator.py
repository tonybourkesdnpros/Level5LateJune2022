import yaml
from cvplibrary import CVPGlobalVariables,GlobalVariableNames
from cvplibrary import RestClient
import ssl 

ssl._create_default_https_context = ssl._create_unverified_context


switch = (CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS))

# hostname = switch['hostname']

for item in switch:
  key, value = item.split(':')
  if key == 'hostname':
    hostname = value
    

cvp_api_url = 'https://192.168.0.5/cvpservice/'
configlet = 'underlay_yaml'

rest_client = RestClient(cvp_api_url+'configlet/getConfigletByName.do?name='+configlet,'GET')

if rest_client.connect():
  raw = rest_client.getResponse()
  
underlay_raw = yaml.safe_load(raw)


underlay_text = underlay_raw['config']

underlay = yaml.safe_load(underlay_text)




MTU = underlay['global']['MTU']

# Global Variables

prefix_list = """
ip prefix-list LOOPBACK
    seq 10 permit 192.168.101.0/24 eq 32
    seq 20 permit 192.168.102.0/24 eq 32
    seq 30 permit 192.168.201.0/24 eq 32
    seq 40 permit 192.168.202.0/24 eq 32
route-map LOOPBACK permit 10
  match ip address prefix-list LOOPBACK
"""
peer_range = """
peer-filter LEAF-AS-RANGE
 10 match as-range 65000-65535 result accept
"""

def gen_int(device):
  for iface in underlay[device]['interfaces']:
    print("interface %s") % iface
    ip = underlay[device]['interfaces'][iface]['ipv4']
    mask = underlay[device]['interfaces'][iface]['mask']
    print("  ip address %s/%s") % (ip, mask)
    if 'thernet' in iface:
      print("  mtu %s") % MTU
      print("  no switchport")
      
def gen_leaf(device):
  
  print("ip virtual-router mac-address 001c.7300.0099")
  print(prefix_list)
  ASN = underlay[device]['BGP']['ASN']
  lo0 = underlay[device]['interfaces']['loopback0']['ipv4']
  print("router bgp %s") % ASN
  print("  router-id %s") % lo0
  print("  no bgp default ipv4-unicast")
  print("  maximum-paths 3")
  print("  distance bgp 20 200 200") 


  print("  neighbor Underlay peer group")
  
  
  DC_list = hostname.split("-")
  DC = DC_list[1]
  
  DC_ASN = underlay['global'][DC]['spine_ASN']
  
  print("  neighbor Underlay remote-as %s") % DC_ASN
  print("  neighbor Underlay send-community")
  print("  neighbor Underlay maximum-routes 12000")
  print("  neighbor LEAF_Peer peer group")
  print("  neighbor LEAF_Peer remote-as %s") % ASN
  print("  neighbor LEAF_Peer next-hop-self")
  print("  neighbor LEAF_Peer maximum-routes 12000")

  for neighbor in underlay[hostname]['BGP']['spine-peers']:
    print("  neighbor %s peer group Underlay") % neighbor

  if underlay[hostname]['MLAG'] == 'Odd':
    print("  neighbor 192.168.255.2 peer group LEAF_Peer")
  if underlay[hostname]['MLAG'] == 'Even':
    print("  neighbor 192.168.255.1 peer group LEAF_Peer")

   
  print("  neighbor EVPN peer group")
 
  print("  neighbor EVPN remote-as %s") % DC_ASN
 
  
  print("  neighbor EVPN update-source Loopback0")
  print("  neighbor EVPN ebgp-multihop 3")
  print("  neighbor EVPN send-community")
  print("  neighbor EVPN maximum-routes 0")
  
  
  for neighbor in underlay['global'][DC]['spine_peers']:
    print("  neighbor %s peer group EVPN") % neighbor

  activate = """
  address-family evpn
    neighbor EVPN activate
   
  address-family ipv4
    neighbor Underlay activate
    neighbor LEAF_Peer activate
    redistribute connected route-map LOOPBACK
  """
  print(activate)
  
def gen_spine_bgp(device):
  print(prefix_list)
  print(peer_range)
  ASN = underlay[hostname]['BGP']['ASN']
  loopback0 = underlay[hostname]['interfaces']['loopback0']['ipv4']
  print("router bgp %s") % ASN  
  
  print("  router-id %s ") % loopback0
  print("  no bgp default ipv4-unicast")
  print("  maximum-paths 3")
  print("  distance bgp 20 200 200")


  range = "192.168.103.0/24"

    
  print("  bgp listen range %s peer-group LEAF_Underlay peer-filter LEAF-AS-RANGE") % range
      
  print(" neighbor LEAF_Underlay peer group")
  print(" neighbor LEAF_Underlay send-community")
  print(" neighbor LEAF_Underlay maximum-routes 12000") 

  

  print("  neighbor EVPN peer group") 

  evpn_range = "192.168.101.0/24"

  print("  bgp listen range %s peer-group EVPN peer-filter LEAF-AS-RANGE") % evpn_range
      
  
  print("  neighbor EVPN update-source Loopback0")
  print("  neighbor EVPN ebgp-multihop 3")
  print("  neighbor EVPN send-community extended")
  print("  neighbor EVPN maximum-routes 0")

  print("  address-family evpn")
  print("    neighbor EVPN activate")
  print("  address-family ipv4")
  print("    neighbor LEAF_Underlay activate")
  print("    redistribute connected route-map LOOPBACK")
  
  
  
  
  
  
  

gen_int(hostname)
  
if 'leaf' in hostname:
  gen_leaf(hostname)
if 'spine' in hostname:
  gen_spine_bgp(hostname)
