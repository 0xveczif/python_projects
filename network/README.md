Here we have multiple programs which can run in http protocol.  
To bypass https and to work for https, run the programs with sslstrip  
  
Example -  
to run packet sniffer  
    - start packet sniffer  
    - start arpspoof.py  
    - start bettercap  
    - bettercap -iface eth0 -caplet hstshijack/hstshijack  

Use same methodology for all programs and change port 80 to 8080  

For inject_code - add one line in request section after load = re.sub // in last line of request.  
			- load = load.replace("HTTP/1.1", "HTTP/1.0")
