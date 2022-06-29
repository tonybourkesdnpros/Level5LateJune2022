
import yaml


raw_yaml = open('underlay.yml', 'r')

underlay = yaml.safe_load(raw_yaml)


for device in underlay['devices']:
    print("-----------------------------------")
    print("This is the config for", device)
    print("")
    for iface in underlay['devices'][device]['interfaces']:
        print("inteface", iface)
        ip = underlay['devices'][device]['interfaces'][iface]
        print("  ip address", ip)
        if 'thernet' in iface:
            print("mtu 9214")