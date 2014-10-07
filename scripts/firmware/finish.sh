#!/bin/bash          

pushd ..

FW_VER="tag_13111500"
echo $FW_VER    
mkdir -pv out/$FW_VER
mkdir -pv out/$FW_VER/add
mkdir -pv out/$FW_VER/bit
find -L . -name "*.xml" -not -path "./work/*"  -not -path "./out/*" -exec cp {} ./out/$FW_VER/add \;
cp ./work/top.bit ./out/$FW_VER/bit
# scp -r out/$FW_VER  hwtest@gct-904-tca:
scp -r out/$FW_VER  hwtest@greg-ttl:
echo "ip128, q18, null algo, new buf" > out/$FW_VER/README.txt 

popd
