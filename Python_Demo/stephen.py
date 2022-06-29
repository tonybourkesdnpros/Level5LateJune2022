from cvprac.cvp_client import CvpClient
from cvprac.cvp_client_errors import CvpApiError
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

cvp1 = '192.168.0.5'
cvp_user = 'arista'
cvp_password = 'aristaifvc'

def get_configlets(mac: str) -> list:
    configlets = []
    for result in client.api.get_configlets_by_device_id(mac):
        configlets.append(result['name'])
    return configlets

client = CvpClient()

client.connect([cvp1], cvp_user, cvp_password)

inventory = client.api.get_inventory()

for item in inventory:
    print(item['hostname']+": "+item['version'])
    print(get_configlets(item['key']))
    print("*"*20)
