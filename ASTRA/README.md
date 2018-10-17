This directory contains ASTRA input files to simulate the FAST photoinjector compiring the 1+1/2 RF gun followed by two SRF cavities up to z=8m from the photocathode. 

A description of the injector design can be found in http://accelconf.web.cern.ch/AccelConf/IPAC10/papers/thpd020.pdf
(note that CAV39 is not anymore part of the nominal setup). 

The current file are as follows:

laser1G.in		input distribution generator (cathode)
magnetized_3p2nC.in	astra input deck for a magnetized beam generation
radial2k_1G.ini		example of input distribution
rfgun_SF2013.dat	E_z(r=0,z) axial field for the gun
sol_alone_100A.dat	B_z(r=0,z) field for the bucking and main solenoids (used by magnetized_3p2nC.in)
fastbothsol_main100A.dat B_z(r=0,z) field for the combined solenoids set to buck the field on the cathode surface (used by roundbeam_1nC.in)
tesla_SF2013.dat	E_z(r=0,z) axial field for the TESLA SRF cavity

