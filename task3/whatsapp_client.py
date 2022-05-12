#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 13:03:13 2021

@author: alex
"""
import socket
import threading
import sys
import random
import os
import subprocess


bufferSize = 1024


#Client Code
def ReceiveData(sock):
    while True:
        try:
            data,addr = sock.recvfrom(bufferSize)
            print(data.decode('utf-8'))
        except:
            pass

def RunClient(serverIP):
    isShared = False
    sharedFolder=0
    isConnected = 0
    path =""
    unpath=""
    print("What is your request:")
    while True:        
        request = input()
        if request == 'mount':
            isConnected = 1
            host = socket.gethostbyname(socket.gethostname())
            port = random.randint(6000, 10000)
            print('Client IP->' + str(host) + ' Port->' + str(port))
            server = (str(serverIP), 5000)
            UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            UDPClientSocket.bind((host, port))
            name = 'make connection to the server'
            UDPClientSocket.sendto(name.encode('utf-8'), server)
            threading.Thread(target=ReceiveData, args=(UDPClientSocket,)).start()

            request = '6' + ' ' + "brcst"
            UDPClientSocket.sendto(request.encode('utf-8'), server)



        elif request == 'qqq':
            break
        elif (request.split(" ")[0]=="share"):
            isShared=True
            sharedFolder=request.split(" ")[1]
            print("you are now sharing")
        else:
            if (not isConnected):
                if(not request.split(" ")[0]=="cd"):
                    request = request.split(' ')
                    k= subprocess.run(request)
                    print(k)
                else:
                    os.chdir(request.split(" ")[1])

            else:
                if(request.split(" ")[0]=="cd"):
                    if(not request.split(" ")[1]==".."):
                        path=path+request.split(" ")[1]+"/"

                        unpath=unpath+"../"

                    else:
                        path_arr = path.split("/")
                        path = "/".join(path_arr[:-2])
                        path = path +"/"

                        unpath_arr=unpath.split("/")
                        unpath="/".join(unpath_arr[:-2])
                        unpath = unpath +"/"

                else:
                    if(request.split(" ")[0]=="cp"):
                        dest=open(request.split(" ")[2],'w')



                    path1 = '1' + ' '+ path
                    request = '5' + ' '+"brcst"+" "+ request
                    unpath1 = '1' + ' '+ unpath

                    UDPClientSocket.sendto(path1.encode('utf-8'), server)
                    UDPClientSocket.sendto(request.encode('utf-8'), server)
                    UDPClientSocket.sendto(unpath1.encode('utf-8'), server)






                    #UDPClientSocket.sendto(data.encode('utf-8'),server)
    dest.close()
    UDPClientSocket.close()
    os._exit(1)
#Client Code Ends Here




if __name__ == '__main__':

    RunClient(sys.argv[1])
    