#!/usr/bin/env python
import libtmux
from sys import argv
import sys
import random
import os


s = libtmux.Server()
s.raise_if_dead()
session = s.sessions[0]
# print(session)
# print('-------')
windows_in_use=set()
windows=session.list_windows()
# session.select_window(0).kill_window()
# w=session.select_window(0).rename_window(argv[2])
for i in windows:
    windows_in_use.add(i.window_index)
if argv[1]=='start':
    #start n
    port=3000

    n=int(argv[2])
    for i in windows_in_use:
        if not os.path.exists(f"dir{i}"):
            os.makedirs(f"dir{i}")
        w=session.select_window(i)
        token = random.getrandbits(128)
        w.attached_pane.send_keys(f"jupyter notebook --port {port + int(i)} --no-browser --NotebookApp.token={token} --NotebookApp.notebook_dir=dir{i}")
        print(f"jupyter notebook number {i}: port {port + int(i)}, token {token}")
        port+=1
    for i in range(len(windows_in_use),n):
        if not os.path.exists(f"dir{i}"):
            os.makedirs(f"dir{i}")
        token = random.getrandbits(128)

        w=session.new_window(attach=False, window_name=f"notebook {i}",
                        start_directory=f"dir{i}",window_index=i)
        w.attached_pane.send_keys(
            f"jupyter notebook --port {port + int(i)} --no-browser --NotebookApp.token={token} --NotebookApp.notebook_dir=dir{i}")
        print(f"jupyter notebook number {i}: port {port + int(i)}, token {token}")
        # print('------------------------------------------------------------------')

        with open('file.txt','w') as file:
            st=''
            for i in range(n):
                st+=str(i)+' '
            file.write(st)
        port+=1

        # s.cmd('tmux detach')
elif len(argv)==2:
    #stap_all
    s.kill_server()
    print('stop_all')
    os.remove('file.txt')
else:
    #stop
    n = int(argv[2])
    with open('file.txt','r') as file:
        st=file.readline().split()
        usd=set()
        index=0
        for i in st:
            if int(i)==n:
                index=1
            else:
                usd.add(i)
    with open('file.txt','w') as file:
        st=''
        for i in usd:
            st+=str(i)+' '
    if index:
        w=session.select_window(n)
        w.kill_window()
        print(f'stopped window {n}')
    else:
        print('no such window')