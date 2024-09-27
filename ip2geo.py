#!/usr/bin/python3

import os, sys, subprocess, ipaddress, shutil

def ip_details(rawip):

    try:
        cmd = "jq"
        cmdpath = shutil.which(cmd)
        if cmdpath is None:
            print("Please install",cmd)
        else:
            ip = ipaddress.ip_address(rawip)
            if ip.is_private:
                print("This is a Private Address")
            else:
                ip = ipaddress.ip_address(rawip)
                if (ip.version == 4) or (ip.version == 6):
                    #The below line broke. Had to make a change. Not sure what the cause is.
                    #command = 'curl http://ipwhois.app/json/{%s} | jq \'"\(.continent) - \(.country) - \(.org)"\'' % (ip)
                    command = 'curl http://ipwhois.app/json/{0} | jq -r \'"\\(.continent) - \\(.country) - \\(.org)"\''.format(ip)
                    runcommand = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    result = (runcommand.stdout)
                    print("%s: %s" % (ip,result))
    
    except:
        lookup = ("host %s | grep 'has address' | awk 'NR==1{print $4}'" % (rawip))
        lookupresult = subprocess.run(lookup, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        ip=(lookupresult.stdout)
        ip=ip.strip()
        #The below line broke. Had to make a change. Not sure what the cause is.
        #command = 'curl http://ipwhois.app/json/{%s} | jq \'"\(.continent) - \(.country) - \(.org)"\'' % (ip)
        command = 'curl http://ipwhois.app/json/{0} | jq -r \'"\\(.continent) - \\(.country) - \\(.org)"\''.format(ip)
        runcommand = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        result = (runcommand.stdout)
        result = result.strip()
        print("%s: %s" % (rawip,result))

if __name__ == '__main__':
    if len(sys.argv) != 1:
        ip_details(sys.argv[1])
    else:
        print("===================")
        print("=IP to Geolocation=")
        print("===================")
        print("Usage: ./ip2geo.py ipaddress")
        print("example: ./ip2geo.py 8.8.8.8")
        print("example: ./ip2geo.py www.google.com")


