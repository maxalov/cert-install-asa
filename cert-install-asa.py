import base64
import configparser
import json
from datetime import datetime

import requests
import urllib3
from OpenSSL import crypto

from authentication import get_auth_token as header

urllib3.disable_warnings()

date_name = datetime.now().strftime("%Y%m%d")
parser = configparser.ConfigParser()
parser.read('config.ini')
ipaddress = parser.get('options', 'ipaddress')
username = parser.get('options', 'username')
password = parser.get('options', 'password')
interface = parser.get('options', 'interface')
cert_path = parser.get('options', 'certpath')
cert_pass = parser.get('options', 'certpass')
cert_name = parser.get('options', 'certname')
pin = parser.get('options', 'pin')


def request_pkcs12(certpath, certpass, certname, datename):
    key_pem = open(certpath + certname + '.key', 'r').read()
    cert_pem = open(certpath + certname + '.cer', 'rb').read()
    ca_pem = open(certpath + 'ca.cer', 'rb').read()

    privkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key_pem)
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_pem)
    ca = [crypto.load_certificate(crypto.FILETYPE_PEM, ca_pem)]

    p12 = crypto.PKCS12()
    p12.set_privatekey(privkey)
    p12.set_certificate(cert)
    p12.set_ca_certificates(ca)
    cert_p12 = p12.export(certpass.encode())

    with open(certpath + datename + '.p12', 'wb') as p12file:
        p12file.write(cert_p12)

    print(f'OPEN SSL Certificate {datename}.p12 successfully created and move to {certpath}')


def convert_postaddcert(certpath, datename, certpass):
    with open(certpath + datename + '.p12', 'rb') as cert:
        encoded_data = base64.b64encode(cert.read())
        decoded_data = encoded_data.decode('utf-8')
    certificate = ['-----BEGIN PKCS12-----']
    while len(decoded_data) > 64:
        certificate.append(decoded_data[:64])
        decoded_data = decoded_data[64:]
    else:
        certificate.append(decoded_data)
    certificate.append('-----END PKCS12-----')
    add_cert = json.dumps(
        {"kind": "object#IdentityCertificate", "name": datename, "certText": certificate, "certPass": certpass})
    return add_cert


def convert_postpincert(datename, nameif):
    command = f'ssl trust-point {datename} {nameif}'
    pin_cert = json.dumps({'commands': [command, 'write']})
    return pin_cert


def post_rest_api(ip, data, datename, nameif, attach=False):
    url = f'https://{ip}/api/certificate/identity'
    token = header(ip, username, password)
    if token:
        print(f'REST API Trying upload ssl certificate {datename}.p12 to cisco ip {ip}')
        ssl_upload = requests.post(url, headers=token, data=data, verify=False)
        print(f'REST API Response {ssl_upload.json()}')
        if attach:
            pin_data = convert_postpincert(datename, nameif)
            url = f'https://{ip}/api/cli'
            print(f'REST API Trying attach ssl certificate {datename}.p12 to cisco ip {ip} nameif {nameif}')
            ssl_pin = requests.post(url, headers=token, data=pin_data, verify=False)
            print(f'REST API Response {ssl_pin.json()}')


def main():
    start_time = datetime.now()
    request_pkcs12(cert_path, cert_pass, cert_name, date_name)
    if pin == 'True':
        post_rest_api(ipaddress, convert_postaddcert(cert_path, date_name, cert_pass), date_name, interface, pin)
    else:
        post_rest_api(ipaddress, convert_postaddcert(cert_path, date_name, cert_pass), date_name, interface)
    print("\nElapsed time: " + str(datetime.now() - start_time))


if __name__ == "__main__":
    main()
