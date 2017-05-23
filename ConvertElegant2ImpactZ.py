import os 
from string import *
from math import *
import sys
import getopt
import numpy as np
import re 


'''
1- first convert your survey file to 
sddsprintout -nolabel -notitle -column=s -column=ElementName -column=ElementType injectortodump.survey  > currentSurvey

2- then run this script

VERY IMPORTANT: we have to make sure the K1 are defined in elegant (as the saved file
                does not have the "K1=" string when K1=0

'''


survey_file =  'currentSurvey'
saved_file  =  'injectortoICS.saved_lattice'
momentum    =  os.popen("sddsanalyzebeam cryomodule_end.out -pipe=out | sdds2stream -pipe -column=pAverage").read()


print ' momentum -------------'
print float(momentum)
print '-------------'
#def dump_quadr_T(L,zstart,index):
#        ZV= "%f" % zstart
#	fh.write ('! Quad #'+index+'\n')
#	fh.write (str(L)+' 10 20  1 '+ZV+' B'+index+'  0. 0.01  0. 0. 0. 0. 0.  /\n')
#
#def dump_drift_T(L,zstart):
#        ZV= "%f" % zstart
#	fh.write (str(L)+' 10 20  0 '+ZV+'  0.0001  /\n')



# load processed survey file:
survey = open(survey_file)
deck_survey = survey.read().splitlines()
survey.close()

# load processed saved file:
saved = open(saved_file)
deck_saved = saved.read().splitlines()
saved.close()


QuadName     = []
QuadStrength = []
QuadLength   = []
DrifName     = []
DrifLength   = []
BendName     = []
BendLength   = []
BendAngle    = []


for line in deck_saved: 
  if "QUAD" in line:
     print "-------- found a quad!"
     print line
     sp1=line.split(':')
     Name=sp1[0]
     # fix an annoying issue with the quote in ELEGANT saved file 
     if '"' in Name:
        Name=Name[1:-1]
     sp2=sp1[1].split(',K1=')
     K1=sp2[1]
     sp3=sp2[0].split(',L=')
     L=sp3[1]
#     print 'quad name    : ', Name
#     print 'quad strength: ', K1
#     print 'quad length  : ', L
     QuadName.append(Name)
     QuadStrength.append(K1)
     QuadLength.append(L)

  if "DRIF" in line:
     print "-------- found a drift!"
     print line
     sp1=line.split(':')
     Name=sp1[0]
     # fix an annoying issue with the quote in ELEGANT saved file 
     if '"' in Name:
        Name=Name[1:-1]
     sp2=sp1[1].split(',L=')
     L=sp2[1]
#     print 'drift name    : ', Name
#     print 'drift length  : ', L
     DrifName.append(Name)
     DrifLength.append(L)
     
  if "SBEN" in line:
     print "found a dipole -----------------!"
     print line
     sp1=line.split(':')
     Name=sp1[0]
     # fix an annoying issue with the quote in ELEGANT saved file 
     if '"' in Name:
        Name=Name[1:-1]
     sp2=sp1[1].split(',L=')
     sp3=sp2[1].split(',ANGLE=')
     L=sp3[0]
     sp4=sp3[1].split(',E1=')
     Angle=sp4[0]
     print 'dipole name    : ', Name
     print 'dipole length  : ', L
     print 'dipole angle   : ', Angle
     BendName.append(Name)
     BendLength.append(L)
     BendAngle.append(Angle)

fo=open ('impactz.lattice','w')

QuadField=np.zeros((len(QuadStrength)))
Length=0.

i=0      
for line in deck_survey: 
  if i==0:
     QuadParam=line.split()
     StartPosition=QuadParam[0]
     OldPosition=QuadParam[0]
  if "QUAD" in line:
     QuadParam=line.split()
#     print QuadParam
     for i in range(len(QuadName)):
        if QuadParam[1]==QuadName[i]:
	   print i
	   print QuadName[i]
	   print QuadStrength[i]
	   print QuadLength[i]
	   CurrentPosition=QuadParam[0]
	   # the -1.00 is to account for different convention between Elegant and Impact*
	   QuadField[i]=-1.00*float(QuadStrength[i])*float(momentum)*0.5109/299.992458;
	   str1= "! ---- quad. " + QuadName[i]
	   str2= "! ----   K1= " + QuadStrength[i]
	   str3= QuadLength[i]+" 4  20    1 "+str(QuadField[i])+" 0. 0.014  0. 0. 0. 0. 0. /" 
	   fo.write(str1+'\n'+str2+'\n'+str3+'\n')
	   Length+=float(QuadLength[i])
  if "DRIF" in line:
     DrifParam=line.split()
#     print DrifParam
     for i in range(len(DrifName)):
        if DrifParam[1]==DrifName[i]:
	   print i
	   print DrifName[i]
	   print DrifLength[i]
	   CurrentPosition=QuadParam[0]
	   str1= "! ---- drift. "+DrifName[i]
	   str2= DrifLength[i]+" 4  20    0 0. 0.014 /" 
	   fo.write(str1+'\n'+str2+'\n')
	   Length+=float(DrifLength[i])
  if "BEN" in line:
     BendParam=line.split()
     print BendParam
     for i in range(len(BendName)):
        if BendParam[1]==BendName[i]:
	   print i
	   print BendName[i]
	   print BendLength[i]
	   print BendAngle[i]
	   CurrentPosition=BendParam[0]
	   str1= "! ---- Bend. "+BendName[i]
	   str2= BendLength[i]+" 4  20  1 "+BendAngle[i]+" 0. 0.014  0. 0. 0. 0. 0. /" 
	   fo.write(str1+'\n'+str2+'\n')
	   Length+=float(BendLength[i])

print "total beamline length: "+str(Length)+" m"
fo.close()

