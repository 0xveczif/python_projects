# #!/usr/bin/env python2
#
# import scapy.all as scapy
# import sys,os, argparse
#
# def check_root():
#     if os.geteuid() != 0:
#         print("Please run the script as root.")
#         sys.exit()
#
# def check_interface_exists(interface):
#     """Check if the interface exists on the system."""
#     interfaces = os.listdir('/sys/class/net/')
#     if interface not in interfaces:
#         print("Error: Interface '{}' not present on this system.".format(interface))
#         print("Available interfaces: {}".format(', '.join(interfaces)))
#         sys.exit(1)
#
# def get_arguments():
#     parser = argparse.ArgumentParser()
#     # parser = optparse.OptionParser()
#     parser.add_argument(dest="interface", help="Interface")
#     options = parser.parse_args()
#     if not options.interface:
#         parser.error("[-] Please Specify Interface. use --help for more info.")
#     return options
#
# def get_mac(ip):
#     arp_request = scapy.ARP(pdst=ip)
#     broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
#     arp_request_broadcast = broadcast/arp_request
#     answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
#     if answered_list:
#         return answered_list[0][1].hwsrc
#     else:
#         print("[!] Failed to get MAC address for {}".format(ip))
#         return None
#
# def sniff(interface):
#     scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
#     #prn=callback function that is called for each sniffed packet. and store=False = not to store sniffed packet in memory
#
# def process_sniffed_packet(packet):
#     if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
#         try:
#             real_mac = get_mac(packet[scapy.ARP].psrc)
#             response_mac = packet[scapy.ARP].hwsrc
#
#             if real_mac != response_mac:
#                 print("\033[93m[+] You are under attack !!!\033[0m")
#             else:
#                 print("[+] Everything safe.")
#
#         except IndexError:
#             pass
#
#
# check_root()
#
# arguments = get_arguments()
# check_interface_exists(arguments.interface)
# print("Started. Scanning ARP table...")
# sniff(arguments.interface)
#
#
#


#!/usr/bin/env python2

import scapy.all as scapy
import sys, os, argparse

def check_root():
    if os.geteuid() != 0:
        print("Please run the script as root.")
        sys.exit()

def check_interface_exists(interface):
    interfaces = os.listdir('/sys/class/net/')
    if interface not in interfaces:
        print("Error: Interface '{}' not present on this system.".format(interface))
        print("Available interfaces: {}".format(', '.join(interfaces)))
        sys.exit(1)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="interface", help="Interface to sniff on")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface. Use --help for more info.")
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        return None

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc

            if real_mac != response_mac:
                print("\033[91m[!] Possible ARP Spoofing Detected!\033[0m")
                print("    IP Address    : {}".format(packet[scapy.ARP].psrc))
                print("    Claimed MAC   : {}".format(response_mac))
                print("    Real MAC      : {}".format(real_mac) + "\n")
            else:
                print("[+] Verified: {} is safe.".format(packet[scapy.ARP].psrc))

        except IndexError:
            pass

check_root()
arguments = get_arguments()
check_interface_exists(arguments.interface)

# Own IP and MAC for fallback
own_ip = scapy.get_if_addr(arguments.interface)
own_mac = scapy.get_if_hwaddr(arguments.interface)

print("Started. Scanning ARP table on interface '{}'\n".format(arguments.interface))
sniff(arguments.interface)
