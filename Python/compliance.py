from cvprac.cvp_client import CvpClient
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


cvp = "192.168.0.5"
cvp_user = "arista"
cvp_pw = "PASSWORD-GOES-HERE"

client = CvpClient()

client.connect([cvp], cvp_user, cvp_pw)

inventory = client.api.get_inventory()
ooc_count = 0

for item in inventory:
   if item['complianceIndication'] == "WARNING":
       print("The switch", item['hostname'], "is out of compliance")
if ooc_count == 0:
    print("All devices are in compliance")
