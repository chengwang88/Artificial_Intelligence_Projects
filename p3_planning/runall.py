import os, sys
import subprocess


for i in range(1,4):
    for j in range(1,11):
        outlog = 'log/' + str(i) + str(j) + '.log'
        cmd = 'python run_search.py -p ' + str(i) + ' -s ' + str(j)
        #os.system(cmd)
        cmd = cmd.split()
        try:
            subprocess.run(cmd, timeout = 1 )
        except subprocess.TimeoutExpired:
            print(outlog+' Timeout')
            continue