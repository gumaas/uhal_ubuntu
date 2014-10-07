#!/bin/bash    
pushd ..

export REPOS_FW_DIR=`pwd`

# Choose what to build here...
export REPOS_BUILD_DIR=`pwd`/mp7_690es/ise14
# export REPOS_BUILD_DIR=`pwd`/cpld/ise14

mkdir work
cd work

# Set up xilinx if not done externally...
#export XILINXD_LICENSE_FILE=2100@caramel.te.rl.ac.uk   # well, whatever is your equivalent to this if any
#export XILINX_BASE=/data/software/Xilinx/14.5/ISE_DS/
#source $XILINX_BASE/settings64.sh

source $REPOS_FW_DIR/ipbus/firmware/example_designs/scripts/setup.sh
#xtclsh $REPOS_BUILD_DIR/build_project.tcl

popd

