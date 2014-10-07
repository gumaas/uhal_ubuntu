#!/bin/bash    

# The repository directory is hardcoded here.  
# User much choose what repository he/she wants to use..
# THis should probably be defined in a local file so that all 
# scripts can access and it remains local to the directory
REPDIR="${HOME}/Development/cms/rep/mp7_v1_0_1"

pushd ..

# Boards
# ln -sf ${REPDIR}/boards/mp7/base_fw/mp7_485/ .
ln -sf ${REPDIR}/boards/mp7/base_fw/mp7_690es/ .
# ln -sf ${REPDIR}/boards/mp7/base_fw/cpld/ .
# ln -sf ${REPDIR}/boards/mp7/pp/mp7_690es/ .
# ln -sf ${REPDIR}/boards/mp7/mp/mp7_690es/ .
# ln -sf ${REPDIR}/boards/mp7/gct3/mp7_690es/ .


# Base firmware
ln -sf ${REPDIR}/components/ipbus/ .
ln -sf ${REPDIR}/components/mp7_ctrl/ .
ln -sf ${REPDIR}/components/mp7_counters/ .
ln -sf ${REPDIR}/components/mp7_xpoint/ .
ln -sf ${REPDIR}/components/opencores_i2c/ .
ln -sf ${REPDIR}/components/mp7_ttc/ .
ln -sf ${REPDIR}/components/mp7_mgt/ .
ln -sf ${REPDIR}/components/mp7_buffers/ .
ln -sf ${REPDIR}/components/mp7_algo/ .
ln -sf ${REPDIR}/components/mp7_preproc/ .
ln -sf ${REPDIR}/components/mp7_spi/ .
ln -sf ${REPDIR}/components/mp7_mezzanine/ .

# Algos
# ln -sf ${REPDIR}/calol2/ .
# ln -sf ${REPDIR}/gct3/ .

popd



