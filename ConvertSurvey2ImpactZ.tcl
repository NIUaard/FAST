#!/bin/sh
# \
exec tclsh "$0" "$@"


# this script convert an elegant suvery output and output from saved configuration 
# into an impact-Z input file (compatible with ImpactZ of 2008)
# created by P. Piot: Fermilab-NIU Fri Oct 16 14:38:54 CDT 2009
# History:
# PP, Oct-16-2009, V1 does not handle skew quad yet... 
# 

if [llength $argv]!=5 {
    puts "\n\n **** Convert an elegant lattice description into an input deck for Impact-Z ****\n\n"
    puts "Error:: this script requires 5 arguments::"
    puts "\t input:\t\t elegant survey file processed using"
    puts "\t \t\t sddsprintout -nolabel -notitle -column=s -column=ElementName -column=ElementType nml_0902_2009.survey > currentSurvey"  
    puts "\t output:\t filename for generated Impact-Z deck"
    puts "\t saved:\t\t elegant saved file (using the save command in .ele file)"
    puts "\t energyMeV:\t beam TOTAL energy in MeV"
    puts "\t bendsDeg:\t chicane bending angle in deg"
    puts "\n\n"
    puts "EXAMPLE\n"
    puts "\n ./ConvertSurvey2ImpactZ.tcl currentSurvey nml.mad nml_0902_2009_fit.new 71 18 \n\n\n\n"
    exit
}

# sddsprintout -nolabel -notitle -column=s -column=ElementName -column=ElementType nml_0902_2009.survey > currentSurvey
# [piot@paris NML_inj_MAR2009]$ ./ConvertSurvey2ImpactZ.tcl currentSurvey nml.mad nml_0902_2009_fit.new 71 18

proc filter {cond list} {
   set res {}
   foreach element $list {if [$cond $element] {lappend res $element}}
   set res
}



set input   	[lindex $argv 0] 
set output  	[lindex $argv 1] 
set saved   	[lindex $argv 2]
set energyMeV   [lindex $argv 3]
set bendsDeg    [lindex $argv 4]


set NPART 200001
set CURRENT 1.000e-10
set gamma [expr $energyMeV / 0.511]
set Kinetic [expr $energyMeV - 0.511]
set Kinetic [expr $Kinetic * 1e6]
set beta  [expr sqrt(1 - 1 / ($gamma * $gamma))]
set bendrd [expr $bendsDeg * acos(-1) / 180.0 ]
set conversion [expr -1.000 / 299.7925 * $beta * $energyMeV ]

puts "gamma $gamma beta $beta bendrd $bendrd" 

set fh [open $saved r]
set i 0 
set j 0
while 1 {
        incr i
	set MyLine [gets $fh line]
	if [eof $fh] break
	set scanErr [scan $line "%s %s" ElemName ElemRest ]
#	puts "$line"
#	puts "$i :: $ElemRest"
	if {[regexp "QUAD" $ElemRest match]}  {
#	   puts "$ElemName here is a quad $ElemRest" 
   	   set scanErr [scan $ElemRest "QUAD,L= %f ,K1= %f " ElemLength ElemStrength ]
	   set ElemName [string map {: {}} $ElemName ] 
	   puts "$ElemName $ElemLength $ElemStrength" 
	   set cmd [concat set $ElemName $ElemStrength]
	   eval $cmd
	}
	if {[regexp "SBEN" $ElemRest match]}  {
   	   set scanErr [scan $ElemRest "SBEN,L= %f ,ANGLE= %f ,&" ElemLength ElemStrength ]
	   set ElemName [string map {: {}} $ElemName ] 
	   puts "$ElemName $ElemLength $ElemStrength" 
	   set cmd [concat set $ElemName $ElemStrength]
	   eval $cmd
	}
#	set [scan $ElemRest "%3s" ElemType]
#	set [scan $ElemRest "%c%c%c,L=%f,K1=%e" ElemType1 ElemType2 ElemType3 ElemLength ]
#	puts "$i :: $ElemName || $ElemRest"
	
     }
close $fh
#exit 

set fp [open $input r]
set fo [open $output w]
set i 0 
set j 0
set indipole 0

# first write header 
puts $fo "!----- to be used with /opt/contrib/piot/Impact_Z/ImpactZser -----"
puts $fo "1 1 "
puts $fo "6  $NPART   1 0 1"
puts $fo "16 16 16 1 0.0140000 0.0140000 0.1025446"
puts $fo "23 0 0 1"
puts $fo "$NPART"  
puts $fo "$CURRENT"   
puts $fo "!q_i/m_i for each charge state. Here, we normalize each charge state q_i=-1 for e-"
puts $fo "-1.956951e-06"
puts $fo "!parameters for initial distribution. NOT USED HERE"
puts $fo "0.001 0.0 0.0  1.000  1.000  0.000  0.000"
puts $fo "0.001 0.0 0.0  1.000  1.000  0.000  0.000"
puts $fo "0.001 0.0 0.0  1.000  1.000  0.000  0.000"
puts $fo "$CURRENT $Kinetic 0.511005e+06  -1.0 1500.0e6 0.0"
puts $fo "!"

puts $fo "!----- lattice (generated with ConvertSurvey2ImpactZ.tcl) E=$energyMeV MeV -----"
while 1 {
        incr i
	set MyLine [gets $fp line]
	if [eof $fh] break
	set L [filter llength $line]
#	puts "$i :: [lindex $L 0] [lindex $L 1]"
	if {$i == 1} {
		set LengthOld [lindex $L 0]
	}
	if {$i>1}	{
		set Length [expr [lindex $L 0] - $LengthOld ]

		if {[lindex $L 2] == "DRIF"}	{
			puts $fo "$Length 4  20    0    0.014  /" 
		}
		if {[lindex $L 2] == "QUAD"}	{
			puts $fo "! quad:: [lindex $L 1]"
			set currentQuad [lindex $L 1]
			set cmd [concat "set currentstrength" "\[expr $conversion * \$$currentQuad \]"]
			eval $cmd 
			puts $fo "$Length 4  20    1 $currentstrength 0. 0.014  0. 0. 0. 0. 0. /" 
		}
		if {[lindex $L 2] == "SBEN"}	{
		        incr indipole
			puts $fo "! dipole:: [lindex $L 1]"
			set currentDipole [lindex $L 1]
			set cmd [concat "set currentstrength" "\$$currentDipole"]
			eval $cmd
			
		        if {$indipole == 1}	{
			   puts $fo "$Length 10  20    4 $currentstrength  0.0 410  0.05 0.0 $currentstrength  0.0 0.0 0.5 /"
			}
		        if {$indipole == 2}	{
			   puts $fo "$Length 10  20    4 $currentstrength  0.0 410  0.05 $currentstrength  0.0 0.0 0.0 0.5 /"
			}
		        if {$indipole == 3}	{
			   puts $fo "$Length 10  20    4 $currentstrength  0.0 410  0.05 0.0 $currentstrength  0.0 0.0 0.5 /"
			}
		        if {$indipole == 4}	{
			   puts $fo "$Length 10  20    4 $currentstrength  0.0 410  0.05 $currentstrength  0.0 0.0 0.0 0.5 /"
			}
		}
		if {[lindex $L 2] == "WATCH"}	{
		        incr j
			puts $fo "! viewer [lindex $L 1]"
			puts $fo "0.0000000  0 100$j  -2    1.00 /"
		}
		set LengthOld [lindex $L 0]
	}
	
     }
     
close $fp
close $fo

