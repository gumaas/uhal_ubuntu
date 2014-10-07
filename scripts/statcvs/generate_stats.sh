#!/bin/bash
export CVSROOT=:pserver:anonymous:98passwd@isscvs.cern.ch:/local/reps/tridas

TMP_DIR=/tmp/generate_stats_l1ts
STATCVS_DIR=/afs/cern.ch/project/l1ts/statcvs
RESULT_DIR=/afs/cern.ch/project/l1ts/www/statcvs

rm -rf $TMP_DIR 
mkdir -p $TMP_DIR 
cd $TMP_DIR 
cvs co -P TriDAS/trigger
cvs co -P TriDAS/RunControl/functionmanagers/dev/LTCFM
cvs co -P TriDAS/RunControl/functionmanagers/dev/gtp
cvs log > cvs.log 

java -mx512m -jar $STATCVS_DIR/statcvs.jar -include "**/*.c;**/*.cc;**/*.cpp;**/*.c++;**/*.h;**/*.hh;**/*.hpp;**/*.java;**/*.py;**/*.pl;**/*.sh;" -exclude "**/csctf/SPValidation/**/*" cvs.log . 
rm -rf cvs.log TriDAS 

rm -rf $RESULT_DIR
mv $TMP_DIR $RESULT_DIR




