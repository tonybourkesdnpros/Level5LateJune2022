import pyeapi

connect = pyeapi.connect_to('internet')

all_vlans = connect.api("vlans").getall()

for vlan in all_vlans:
    print(all_vlans[vlan]['vlan_id'])