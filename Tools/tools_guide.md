### Tools Guide

<pre>

Introduction and Setup
	1. Some systems only have or programs written on python2 and need to write or run with python2.
	2. To run =
		1. terminal - python hello.py
		2. python3 hello.py
		3. or chmod +x hello.py - ./hello.py
	3. Use Python Editor for writing a large and complex programs and debugging them
		1. Pycharm
			1. https://www.jetbrains.com/pycharm/download/?section=linux
			2. download community version
			3. Unzip and put in opt directory - all tools we put there
			4. sudo cp -r  pycharm-community-2025.1.1.1 /opt/
			5. cd /opt/pycharm-community-2025.1.1.1/bin
			6. ./pycharm.sh

Netfilterqueue - for python 2.7 - Installing netfilterqueue for python2.  2.7.18
	We have python3.13 and it is not supported in that.
	- Update
		- sudo apt update
		- sudo apt upgrade -y
		- sudo apt full upgrade -y
	- install dependencies
		- sudo apt install python2 python2-dev libnetfilter-queue-dev
			  // > These are **required** to compile the C extension.
	- Install through git
		- git clone https://github.com/kti/python-netfilterqueue.git
		- cd python-netfilterqueue
	- Install dependency - cython
		- sudo python2 -m pip install "Cython<0.29" 
				// downloading cython older version so that it supports our library libnetfilter, dependency and module netfilterqueue
	- open setup.py with mousepad and change these lines with this
		- compiler_directives={"language_level": 2},
		- exec(open("netfilterqueue/_version.py").read())
	- build and run
		- sudo python2 setup.py build
		- sudo python2 setup.py install

Scapy - for python 2.7 - 2.7.18 - installations
	- `sudo python2 -m pip install --upgrade pip==20.3.4 setuptools==44.1.1 wheel`
	- `sudo python2 -m pip install scapy==2.4.3 `
	- If pip is broken
		- wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
		- sudo python2 get-pip.py
		- pip install --upgrade pip
		- pip install scapy_http
		- pip install scapy-http

pynput
		> pip install pynput

Lazagne projects-
	Password extractor tool
	https://github.com/AlessandroZ/LaZagne
	download - unzip
	if we r unsure about target system architecture. just use 32 bit it will run on both
	use -lazagne.exe --help
	lazagne.exe browsers --help
	all

Regex -
	- search() - search the first occurrance
	- findall() - search all occurances
	- we use () in regex to grouping - group 1 group 2 etc to what when to use
	- ?: - ignore this group
	- print(finding.group(1))              ...it alswo starts from 0, but here we want group 1 result
	- \s - space
	- \s* - all after space

Bypass HTTPS
	- SSLstrip a great toolwritten by someone placed between router and client which tells server that I am communicating with https and to victim, I can communicate with http - https downgrade to http.
	- it will still not work for hsts.
	- USe all programs we created with sslstrip.
	- As original ssltrip is not maintained and will be outdated, we will use bettercap to fulfill our goals.
	- Running
	- Packet sniffer-
		- start packet sniffer
		- start arpspoof.py
		- start bettercap
			- bettercap -iface eth0 -caplet hstshijack/hstshijack
	- Replace downloads
		- start arpspoof
		- start bettercap same as above
		- start iptables routing Forward or Input/output
		- change in code from 80 to 8080
			- // as bettercap proxy over 8080
		- for https, it is oserved that it stucks in loop for checking exe and replacing with exe, to come out of loop, we have to apply if condtition as
			- modify line with
				- if b".exe" in scapy_packet[scapy.Raw].load and b"10.0.2.16" not in scapy_packet[scapy.Raw].load
				- // include ip of target that we include in file.
	- Code injector
		- run all 3 commands as above
		- arpspoof, bettercap,iptables-input+output / forward
		- change 80 to 8080
		- add one line in request section after load = re.sub // in last line of request.
			- load = load.replace("HTTP/1.1", "HTTP/1.0")

Create passcode for mail and to test in malwares-
	- We need to create another app password to use mail server
	- login to account from which we want to send mail -
	- account.google.on - security - signing in to google - app password
	- click - select other enter any name - generate -  got password copy and use it.

Test
	- try in browser http://www.bing.com
	- terminal
	- ping 8.8.8.8
	- ping google.com    // 
	- ping www.bing.com
	- nslookup www.bing.com
		- here we will see our KALI VM IP - 10.0.2.16

</pre>     
	
