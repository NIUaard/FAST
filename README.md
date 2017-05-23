This directory contains a set of ELEGANT file and associated script to simulate
the beam dynamics throughout the Fermilab Accelerator Science & Technology
(FAST) facility. The lattice files used were generated from survey data and
drawings and where provided by Dan Broemmelsek (vesion of 2/23). These files
are constantly update so use at your own risk. 

Before running the mainscript you will have to open the LINES.lte in
All_Lines_edited and update the absolute paths in the INCLUDE statement 
to reflect the locations of the files on your system.

The curent directory tree is as follows:
- Documentation contains a pdf file with instructions on how to run the
simulations. 
- All_Lines_edited contains all the lattice file provided by Dan Bromelsiek. The
file were updated to have Q107, Q107, Q111 skewed, and several fit point were
added. 
- QuadrupoleScanInjector contains instructions on how to peform a quadrupole
scan in the injector by controling the phase advance between the last dipole of
the BC1 chicane and the X121 viewe using three quadupoles. 

