import os,sys


flag = False

out = []
with open('out.log') as f:
    for lines in f:
        if lines[0:4] == 'Solv':
            line = lines[:-4].split()
            out.append(line[4])
            out.append(" ".join(line[6:]))
            print(line)
        if lines[0:4] == 'Expa':
            flag = True
            continue
        if flag:
            line = lines.split()
            out.extend(line)
            print(line)
            flag = False
        if lines[0:4] == 'Plan':
            line = lines.split()
            out.append(line[2])
            out.append(str(round(float(line[-1]),3)))
            print(line)

n = int(len(out)/7)
for i in range(n):
    print(','.join(out[i* 7 :(i+1) * 7]))
