#!/bin/bash

# Assume current username matches SVN username.  May not be the case.
SVNUSER=${USER}
echo "-- Will use username \"${SVNUSER}\" for SVN checkout"

# Path to directory containing all the checked out versions of the repos.
# To disnguish different version of the repbos I use YYMMDDVV, where 
# VV = version on that day.  Choose whatever you like...
# THis should probably be defined in a local file so that all 
# scripts can access and it remains local to the directory
REPDIR="${HOME}/Development/cms/rep/scripts_13111800"
echo "-- Checking out to \"${REPDIR}\""

mkdir -pv "${REPDIR}"
pushd ${REPDIR}

# Edit this to get the correct files...
#svn co svn+ssh://${SVNUSER}@svn.cern.ch/reps/cactus/tags/mp7/mp7_v1_0_1/boards
#svn co svn+ssh://${SVNUSER}@svn.cern.ch/reps/cactus/tags/mp7/mp7_v1_0_1/components

# svn co svn+ssh://${SVNUSER}@svn.cern.ch/reps/cactus/trunk/boards
# svn co svn+ssh://${SVNUSER}@svn.cern.ch/reps/cactus/trunk/components
# svn co svn+ssh://${SVNUSER}@svn.cern.ch/reps/cactus/trunk/cactusprojects/calol2

svn co svn+ssh://${SVNUSER}@svn.cern.ch/reps/cactus/trunk/scripts

popd
