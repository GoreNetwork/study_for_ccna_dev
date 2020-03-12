import requests
from requests.auth import HTTPBasicAuth
import json

DNAC_USER='devnetuser'
DNAC_PASSWORD='Cisco123!'
DNAC=controller_ip='sandboxdnac.cisco.com'
from pprint import pprint
def get_auth_token(controller_ip=DNAC, username=DNAC_USER, password=DNAC_PASSWORD):
	""" Authenticates with controller and returns a token to be used in subsequent API invocations
	"""
	
	login_url = "https://{0}/dna/system/api/v1/auth/token".format(controller_ip)
	result = requests.post(url=login_url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify=False)
	result.raise_for_status()
	
	token = result.json()["Token"]
	return {
		"controller_ip": controller_ip,
		"token": token
	}

def create_url(path, controller_ip=DNAC):
    """ Helper function to create a DNAC API endpoint URL
    """

    return "https://%s/api/v1/%s" % (controller_ip, path)

def list_network_devices():
    return get_url("network-device")

def get_url(url):

    url = create_url(path=url)
    print(url)
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()

print(get_auth_token())

response = list_network_devices()
pprint (response)