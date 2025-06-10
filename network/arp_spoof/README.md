ARP Spoof is a program in which we target router and target system ip and through the program we spoof MAC address of them and we become MITM.
We spoof ourself as router to target and target to router by changing MAC addres to ARP table.

usage - sudo python3 arpspoof eth0 ip(router/gateway) ip(target)
Example - sudo python3 arpspoof eth0 10.0.2.1 10.0.2.15

Requirements - install required libraries. For help, refer tools section
