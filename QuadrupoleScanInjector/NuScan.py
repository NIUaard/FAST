import numpy as np
import os

Npoints = 3

nux=0.00*np.linspace(-0.5, 0.5, Npoints)+0.3
nuy=np.linspace( 0.5, 0.7, Npoints)



fh=open ('nuscan.txt','w')


for i in range(Npoints):
   print str(nux[i])+',nuy='+str(nuy[i])
   command='elegant injector_cryo_nuXY.ele -macro=nux='+str(nux[i])+',nuy='+str(nuy[i])
   os.system(command)
   
   command='sddsprintout -col=ElementName -col=R11 injector_cryo_nuXY.mat| awk \'$1 == "X121" { print $2 }\' ' 
   R11=float(os.popen(command).read())
   command='sddsprintout -col=ElementName -col=R12 injector_cryo_nuXY.mat| awk \'$1 == "X121" { print $2 }\' ' 
   R12=float(os.popen(command).read())
   command='sddsprintout -col=ElementName -col=R13 injector_cryo_nuXY.mat| awk \'$1 == "X121" { print $2 }\' ' 
   R13=float(os.popen(command).read())
   command='sddsprintout -col=ElementName -col=R14 injector_cryo_nuXY.mat| awk \'$1 == "X121" { print $2 }\' ' 
   R14=float(os.popen(command).read())
   command='sddsprintout -col=ElementName -col=R31 injector_cryo_nuXY.mat| awk \'$1 == "X121" { print $2 }\' ' 
   R31=float(os.popen(command).read())
   command='sddsprintout -col=ElementName -col=R32 injector_cryo_nuXY.mat| awk \'$1 == "X121" { print $2 }\' ' 
   R32=float(os.popen(command).read())
   command='sddsprintout -col=ElementName -col=R33 injector_cryo_nuXY.mat| awk \'$1 == "X121" { print $2 }\' ' 
   R33=float(os.popen(command).read())
   command='sddsprintout -col=ElementName -col=R34 injector_cryo_nuXY.mat| awk \'$1 == "X121" { print $2 }\' ' 
   R34=float(os.popen(command).read())


   command='sddsanalyzebeam injector_cryo_nuXY.X121 -pipe=out | sdds2stream   -col=Sx -pipe=in' 
   Sx=float(os.popen(command).read())

   command='sddsanalyzebeam injector_cryo_nuXY.X121 -pipe=out | sdds2stream   -col=Sy -pipe=in' 
   Sy=float(os.popen(command).read())

   command='sddsanalyzebeam injector_cryo_nuXY.X121 -pipe=out | sdds2stream   -col=s12 -pipe=in' 
   s12=float(os.popen(command).read())


   fh.write(str(i)+'\t'+str(R11)+'\t'+str(R12)+'\t'+str(R13)+'\t'+str(R14)+'\t'  \
                       +str(R31)+'\t'+str(R32)+'\t'+str(R33)+'\t'+str(R34)+'\t'  \
                       + str(Sx)+'\t'+ str(Sy)+'\t'+str(s12)+'\n')
		        


fh.close()
