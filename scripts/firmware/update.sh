#!/bin/bash    

# THis should probably be defined in a local file so that all 
# scripts can access and it remains local to the directory
REPDIR="${HOME}/Development/cms/rep/test_13111000"

svn update ${REPDIR}/boards
svn update ${REPDIR}/components
# svn update ${REPDIR}/calol2
