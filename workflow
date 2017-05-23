./clean_directory
elegant injector_cryo.ele 
elegant cryotoFODOend.ele 
elegant FODOend_todump.ele
elegant track_injectortoHEdump.ele 
sddsplot -graph=line,vary -col=s,"beta?" injector.twi  
sddsplot -graph=line,vary -col=s,"beta?" acm.twi  
sddsplot -col=s,etax eid.twi
sddsplot -graph=line,vary -col=s,beta?  eid.twi
~/bin/sddsplottwiss track_injectortoHEdump 60 -limit=ymax=80
