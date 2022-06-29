

from cvprac.cvp_client import CvpClient
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

cvp1 = '192.168.0.5'
cvp_user = 'arista'
cvp_password = 'aristaifvc'

client = CvpClient()

client.connect([cvp1], cvp_user, cvp_password)

inventory = client.api.remove_configlets_from_device(app_name, dev, del_configlets)

for device in inventory:
    base_configlet = device['hostname']+'-BASE'
    print(base_configlet)