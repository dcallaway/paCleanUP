"""
Discription: 
    Palo alto firewalls api does not expose a way to delete software from devices.
    since pa200 have such tiny harddrives it is often nessary to delete all previous
    downlaoded or uploaded images from the device. 
    
    Make a file with one firewall address
    per line set the defaults in the defauts section below.

Requires:
    getpass
    netmiko
    requests
    json
    xmltodict
        
        to install try: pip install netmiko xmltodict requests 

Author:
    Devin Callaway dcallaway@compunet.biz

Tested:
    Tested on macos 12.12.6
    osx system python: 2.7.10
    pa220

Example usage:
    Set default filename username and global timeout in default section below
        $ python deleteUnusedSoftware.py
        Password: 

Cautions:
    Diffrent firewalls my require an adjustment to delay factor on any given command
    PA220 
    4 for connection 
    10 for system info
    15 for software info

Legal:
    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

Todo:
    * change the loop to a fuction so not useing continue:
    * test on multiple plaforms
    * change it up to take a csv with diffrent usernames and passwords per firewall.
"""

from __future__ import print_function, unicode_literals

from netmiko import Netmiko
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
import requests
import json
import xmltodict
from requests.packages.urllib3.exceptions import InsecureRequestWarning 


#############################
#    SET DEFAULTS HERE
#############################

username = "dcallaway"
global_delay_factor = 4
filename = "firewalls2.txt"
password = getpass()
#set commitChange to True or False depending if you want this script to actully delete the software. 
commitChange = False

#############################
#    END DEFAULTS
#############################

#disable RequestWarning because nobody has there certs in order on managment interface
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    firewalls = open(filename)
except: 
    print("Please configure default settings with a file firewalls.txt with one hostname per line and configure defaut username and password.")
    exit()
print ("Opening " + filename)
if commitChange:
    print ("Not a testrun, script will make canges")
else:    
    print ("Test run: no changes will be made")

#loop threw each line in filename:
for aline in firewalls:
    #clean up trailing spaces: or this is left over from when i was doing cvs, cant rembmer. 
    currentFirewall = aline.split()
    currentFirewall = currentFirewall[0]

    #set dict up for netmikko connection:
    my_device = {
        'host': currentFirewall,
        'username': username,
        'password': password,   
        'device_type': 'paloalto_panos',
        'global_delay_factor': global_delay_factor
    }

    #set up request session to firewall API
    connectionString = 'https://' + currentFirewall + "/api"
    uri = connectionString
    s = requests.session()
    s.verify = False

    # get our API KEY and error out if bad connection or password
    try:
        parameters = {"type": "keygen", "user": username ,"password": password}
        response = s.get(uri, params=parameters)
    except:
        print("Can not get API key from firwall:" + currentFirewall)
        continue
    
    #convert the XML into dict because: xml
    d = xmltodict.parse(response.text)
    key = d['response']['result']['key']
    
    #Connect to device via SSH
    print ("Establishing SSH connection to device: " + currentFirewall)
    try:
        net_connect = Netmiko(**my_device)
    except NetMikoTimeoutException:
        print('\n\n\nERROR: Can not connect to Device:' + currentFirewall + "\n\n\n")  
        continue   ###go to top of loop if we cant connect.  
    except NetMikoAuthenticationException:
        print('\n\n\nERROR: Bad username or password:' + currentFirewall + "\n\n\n")
        continue   ###go to top of loop if we cant connect. 
    #setup API request to get software info
    params = {'type': 'op', 'cmd': '<request><system><software><info></info></software></system></request>', 'key': key}
    r = s.get(uri, params=params)

    #print this var if you get lost in json
    versionSonReadable = json.dumps(xmltodict.parse(r.text), indent=4)

    #convert the XML into dict because: xml
    versionSon = xmltodict.parse(r.text)

    #loop threw output and send delete software command to device.    
    for item in versionSon["response"]["result"]["sw-updates"]["versions"]["entry"]:
        if item["current"] == "yes":
            continue
        if item["downloaded"] == "yes" or item["uploaded"] == "yes":
            commandString = ("delete software version " + item["version"])
            print ("sending commnad to device: " + commandString + "\n")
            if commitChange:
                net_connect.send_command(commandString, delay_factor=10)

    #close ssh conection.
    print("closeing connections\n\n\n\n")
    net_connect.disconnect()
    s.close()

print ("closeing " + filename)
firewalls.close()