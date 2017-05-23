#!/usr/bin/python
import os
from string import *
from math import *
import sys
import getopt

os.system("sddsprintout -noLabel -notitle -column=Z -column=ElementType ilctajun06_injector.survey > /tmp/toutput");

Lq=0.102
offset = 0.0001
# get momentum by doing a sddsprintout -parameter=pCentral of input beam. 
Momentum = 82.160

FILE_LATTICE = 'ilctajun06_injector_fit.new'

fh = open("/tmp/tmpImpact","w")


def dump_quadr(L,zstart,index):
        ZV= "%f" % zstart
	fh.write ('! Quad #'+index+'\n')
	fh.write (str(L)+' 10 20  1 '+ZV+' B'+index+'  0. 0.01  0. 0. 0. 0. 0.  /\n')

def dump_drift(L,zstart):
        ZV= "%f" % zstart
	fh.write (str(L)+' 10 20  0 '+ZV+'  0.0001  /\n')
f = open("/tmp/toutput")

zold=0
index=0
index2=0
for line in f:
	tmp = line.split ('       ')
	if len(tmp)==2:
#		print tmp
		if tmp[1]=='  DRIF \n':
		        index2 = index2 + 1
			if index2 == 1:
				dump_drift(float(tmp[0])-float(zold)-float(zold), float(tmp[0])+float(offset))
			if index2 > 1:
				dump_drift(float(tmp[0])-float(zold), float(tmp[0])+float(offset))
#			print float(tmp[0])
		if tmp[1]=='  QUAD \n':
			dump_quadr(Lq, float(tmp[0])+float(offset),str(index))
#			print tmp[0]
		        index = index + 1
		zold=tmp[0]
f.close()
fh.close()

f = open(FILE_LATTICE)

firsttime=0
Variable = []
for line in f:
#        print line,
        tmp1 = line.split ('K1=')
#	print tmp1
        if len(tmp1) == 2 :
#               print firsttime
#                tmp2=tmp1[1].split('\n')
                tmp2=tmp1[1].split('\n')
                VVV=tmp2[0]
                VV=VVV.split('!')
#		print VV
		V = VV[0]
                print firsttime, V
                Variable.append(V)
f.close()

f = open("/tmp/tmpImpact")
deck = f.read()
f.close()

for i in range(len(Variable)):
        ind= len(Variable) - i - 1
        iV = "%s" % (ind) # need to reverse order to make B1 does mix up all the B1* flags 
	print iV
#       Quads_B(i)=x(i)*beta*P/Cm; %currents in Amps
	BField=float(Variable[ind])*float(Momentum)*0.5109/299.992458; 
        deck = replace(deck,'B'+iV, "%e  " % BField)

f = open("/tmp/tmpImpact2",'w')
f.write(deck)
f.close()
