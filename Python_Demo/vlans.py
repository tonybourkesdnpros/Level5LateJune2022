import pyeapi

connect = pyeapi.connect_to('internet')

file = open('vlans.list', 'r')

vlan_list = file.readlines()

for vlan_id in vlan_list:
    result = connect.api("vlans").create(vlan_id)
    if result == True:
        print("Create VLAN", vlan_id)
    else:
        print("Error")