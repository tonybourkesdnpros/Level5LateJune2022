
import pyeapi

connect = pyeapi.connect_to('internet')

result = connect.api("ipinterfaces").create("Ethernet2")

if result == True:
    print("Interface set to L3")
else:
    print("Something went wrong")

    
result = connect.api("ipinterfaces").set_address("Ethernet2", '2.2.2.2/24')



if result == True:
    print("Success!")
else:
    print("Something went wrong")