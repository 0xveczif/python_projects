#!/usr/bin/env python3

import subprocess
import optparse
import re
import os,sys


# get input from user via single command
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC Address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    # option variable contains wlan0, 00:11:22:33:44:55 values and arguments contain interface, new_mac arguments
    if not options.interface:
        parser.error("[-] Please Specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info")
    check_mac(options.new_mac)
    check_interface_exists(options.interface)
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    #   result come into group, search terms will be 1st in group 0, term 2 will be in group 1 etc.
    else:
        print("[-] Could not read MAC address")


def start():
    options = get_arguments()

    current_mac = get_current_mac(options.interface)  # original mac

    if current_mac != options.new_mac:
        print("Current MAC = " + str(current_mac))
        # we are using string to handle error, kif we didn't get return value = none // casting object into string

        change_mac(options.interface, options.new_mac)

        current_mac = get_current_mac(options.interface)  # mac after changing, assigning to same variable
        if current_mac == options.new_mac:
            print("[-] MAC address is successfully changed to " + current_mac)
        else:
            print("[-] MAC address didn't changed")
    else:
        print("MAC address is already set to your need")

    # to run = python macchanger.py
    # sudo python2 macchanger.py -i eth0 -m 00:11:22:33:44:55
    # to run for python 3 =  we need to make some changes only
    # to get changes = run python3 macchanger.py and we will get errors solve those errors and we are done
    # mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))


def check_root():
    if os.geteuid() == 0:
        start()
    else:
        print("Please run the script as root.")

def check_mac(mac):
    """Check and validate MAC address format."""
    if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', mac):
        print("Error: Invalid MAC address format.")
        sys.exit(1)

def check_interface_exists(interface):
    """Check if the interface exists on the system."""
    interfaces = os.listdir('/sys/class/net/')
    if interface not in interfaces:
        print("Error: Interface '{}' not present on this system.".format(interface))
        print("Available interfaces: {}".format(', '.join(interfaces)))
        sys.exit(1)

check_root()
