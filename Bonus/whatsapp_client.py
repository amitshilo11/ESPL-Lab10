#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 13:03:13 2021

@author: alex
"""
import shutil
import socket
import threading
import sys
import random
import os
import subprocess

isShared=False
shared=0
dest="venv/bin/copied.txt"
dfile=open(dest,'w')
dfile.close()
bufferSize = 1024
def find_file(fileName):
    for (root, dirs, files) in os.walk(shared):
        if fileName in files:
            return root + "/" + fileName
    return 0

# Client Code
def ReceiveData(sock,folder=None):
    while True:
        try:
            data, addr = sock.recvfrom(bufferSize)
            if(not data.split(" ")[0]=="1"):
                print(data.decode('utf-8'))
            else:
                path=find_file(data.split(" ")[1])
                if (path != 0):
                    shutil.copy(path,dest)


        except:
            pass


def RunClient(serverIP):
    isConnected = 0
    path = ""
    unpath = ""
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
            data = '10' + ' ' + "bcst"
            UDPClientSocket.sendto(data.encode('utf-8'),server)

        elif request == 'qqq':
            break
        else:

            if (not isConnected):
                if (request.split(" ")[0] == "share"):
                    isShared=True
                    shared=request.split(" ")[1]

                elif (not request.split(" ")[0] == "cd"):
                    request = request.split(' ')
                    k = subprocess.run(request)
                    print(k)
                else:
                    os.chdir(request.split(" ")[1])

            else:
                if (request.split(" ")[0] == "cd"):
                    if (not request.split(" ")[1] == ".."):
                        path = path + request.split(" ")[1] + "/"

                        unpath = unpath + "../"

                    else:
                        path_arr = path.split("/")
                        path = "/".join(path_arr[:-2])
                        path = path + "/"

                        unpath_arr = unpath.split("/")
                        unpath = "/".join(unpath_arr[:-2])
                        unpath = unpath + "/"
                elif (request.split(" ")[0] == "find"):
                    request = '7' + ' ' + request
                    UDPClientSocket.sendto(request.encode('utf-8'), server)


                else:
                    if (request.split(" ")[0] == "cp"):
                        dest = open(request.split(" ")[2], 'w')

                    path1 = '1' + ' ' + path
                    request = '2' + ' ' + request
                    unpath1 = '1' + ' ' + unpath

                    UDPClientSocket.sendto(path1.encode('utf-8'), server)
                    UDPClientSocket.sendto(request.encode('utf-8'), server)
                    UDPClientSocket.sendto(unpath1.encode('utf-8'), server)

                    # UDPClientSocket.sendto(data.encode('utf-8'),server)
    dest.close()

    UDPClientSocket.close()
    os._exit(1)


# Client Code Ends Here


if __name__ == '__main__':
    RunClient(sys.argv[1])
