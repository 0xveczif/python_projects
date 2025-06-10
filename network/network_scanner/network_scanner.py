#!/usr/bin/env python

import scapy.all as scapy
import argparse
#import optparse

def get_arguments():
    parser = argparse.ArgumentParser()
        #parser = optparse.OptionParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range")
        #parser.add_option("-t", "--target", dest="target", help="Target IP / IP range")
    options = parser.parse_args()
        #(options, arguments) = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
     #scapy.ls(scapy.ARP())
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
      #it is broadcast mac address, every device accepts it
      # scapy.ls(scapy.Ether())
      #creating packet that contains mac and ip
    arp_request_broadcast = broadcast/arp_request
     #creating list of response received
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
     #it returns 2 results, we can keep as answered - response received from those ips and unanswered - noone responds to our broadcast
     # answered_list, unanswered_list

    clients_list = []
    for element in answered_list:
        clients_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
         #element[1] because we only deal with answer, it has (request,answer) as response
         #saving list in dictonaries
        clients_list.append(clients_dict)
    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)
