# Script for automatic installation ssl identity certificate on the Cisco ASA via REST API
Allows you to simply convert `private key, cert and .ca` to `.PKCS12` and upload to device
# Filling config.ini
```
[options]
# Management ip address of cisco asa 
ipaddress = 192.168.1.1 
# Credentionals. Be sure, that your account has admin rights.
username = admin
password = superpassword
# Interface cisco asa, on which anyconnect works. 
interface = outside
# Path to private key, cert and chain.
certpath = /Users/vasya.pupkin/folder/
# Password for pkcs12. Be sure, that it's not 'root' or 'qwerty'
certpass = supersecret
# Files names 
certname = supername
# Upload certificate to cisco asa with or without pinning to interface 
pin = True
```
# Run script
python cert-install-asa.py
```
OPEN SSL Certificate 20200316.p12 successfully created and move to /Users/vasya.pupkin/folder/
REST API starts uploading ssl certificate 20200316.p12 to cisco ip 192.168.1.1
REST API response {'messages': [{'level': 'Warning', 'code': '', 'details': 'Import PKCS12 operation completed successfully.'}]}
REST API starts attaching ssl certificate 20200316.p12 to cisco ip 192.168.1.1 interface nameif outside
REST API response {'response': ['', 'Building configuration...\nCryptochecksum: fe1ed704 b7cf5ea3 91d452de 6b8cd26e \n\n24376 bytes copied in 0.290 secs\n[OK]\n']}

Elapsed time: 0:00:19.558316
```
