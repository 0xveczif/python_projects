#!/usr/bin/env python

import requests

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "testfire.net"

try:
    #with open("https://github.com/n0kovo/n0kovo_subdomains/blob/main/n0kovo_subdomains_huge.txt")
    #with open("/root/Downloads/Subdomain.list", "r") as wordlist_file:
    with open("/home/kali/Downloads/n0kovo_subdomains_small.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = word + "." + target_url
            response = request(test_url)
            if response:
                print("[+] Discovered subdomain --> " + test_url)
except KeyboardInterrupt:
    print("\n[-] Exiting fromm program...")



