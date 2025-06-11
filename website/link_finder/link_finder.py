#Program helps finding all links in website going reccursively to the links find


#!/usr/bin/python

import requests
import re
import urlparse

target_url = "http://testfire.net"

target_links = []

def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', response.content)

def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urlparse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)
try:
    crawl(target_url)
except KeyboardInterrupt:
    print("\n[-] Exiting fromm program...")
