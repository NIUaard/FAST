This directory contains a set of ELEGANT file and associated script to simulate
the beam dynamics throughout the Fermilab Accelerator Science & Technology
(FAST) facility. The lattice files used were generated from survey data and
drawings and where provided by Dan broemmelsiek (version of 2/23/16). These files are regularly updated. 

Before running the main script you will have to open the LINES.lte in
All_Lines_edited and update the absolute paths in the INCLUDE statement 
to reflect the locations of the files on your system. If all is configured properly, you can run one of the workflow* scripts to display several sddswindow showing the beam evolution along the FAST-injector linac. 

The curent directory tree is as follows:
- Documentation contains a pdf file with instructions on how to run the
simulations. 
- All_Lines_edited contains all the lattice files. The files were updated to have Q107, Q107, Q111 skewed, and several fit point were added (compared to the original files). 
- QuadrupoleScanInjector contains instructions on how to peform a quadrupole
scan in the injector by controling the phase advance between the last dipole of
the BC1 chicane and the X121 viewe using three quadupoles. 

