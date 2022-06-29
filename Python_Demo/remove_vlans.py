import pyeapi

connect = pyeapi.connect_to('internet')

file = open('remove_vlans.list', 'r')

vlan_list = file.readlines()
for vlan_id in vlan_list:
    result = connect.api("vlans").delete(vlan_id)
    if result == True:
        print("Remove VLAN", vlan_id)
    else:
        print("Error")